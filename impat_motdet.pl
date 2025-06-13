#!/usr/bin/perl
#!/usr/bin/env perl

use CGI::Fast qw(:standard);
use CGI qw(:standard);
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Session;
use POSIX;
use Data::Dumper;
print header;

print start_html("Results");

$session = CGI::Session->load();
$timenow=time;
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst)=gmtime;
srand(time);
$ran=int(rand(98))+1;
$session=$yday.$hour.$min.$ran;
#print $session;

my $q = new CGI;

$input = $q->param('inputOption');
$up = $q->param('up');
$down = $q->param('down');
$idt = $q->param('idtype');
$genes = $q->param('Gene_ID');
$spp = $q->param('species');
$sequence = $q->param('sequence');
#print scalar(@seq);
#$seq = join("\n", @$seq);

@query = $q->param('query');
foreach $mtf(@query){
    $query .= "$mtf,";
}
$cpe = $q->param('motif');
#print "cpe === $cpe.........motif ==== $query -------------------";
if(($cpe ne "") && ($query ne "")){
    $motif = "$cpe,"."$query";
    $motifType = "query";
    $mtf = $motif;
}elsif (($cpe eq "") && ($query ne "")){
    $motif = $query;
    $motifType = "query";
    $mtf = $motif;
}elsif(($query eq "") && ($cpe ne "")){
    $motif = $cpe;
    $motifType = "query";
    $mtf = $motif;
}elsif(($query eq "") && ($cpe eq "")){
    $motifType = "pfm";
    $pfm = "./JASPAR2024_CORE_non-redundant_pfms_jaspar.txt";
    $mtf = $pfm;
}
sub connect_motdet{
    my ($motif, $pfm, $seq, $session) = @_;

    if ($motif eq ""){
        $script_to_call1 = "sigvarv3.pl pfm '$pfm' '$seq' $session";
        $script_to_call2 = "covar.pl pfm '$pfm' '$seq' $session";
        $script_to_call3 = "submotif.pl pfm '$pfm' '$seq' $session";
    }else{
        $script_to_call1 = "sigvarv3.pl query '$motif' '$seq' $session";
        $script_to_call2 = "covar.pl query '$motif' '$seq' $session";
        $script_to_call3 = "submotif.pl query $motif '$seq' $session";
    }
#print "motif/pfm --> $motif $pfm            seq --> $seq.................";

    my $sigvar_out = qx{$^X $script_to_call1};
    @sigvar = split(/#/, $sigvar_out);

    my $covar_out = qx{$^X $script_to_call2};
    @covar = split(/#/, $covar_out);


    my $submotif_out = qx{$^X $script_to_call3};
    @submotif = split(/#/, $submotif_out);


    # CpG Island Integration
    my $cpg_input_file  = "temp/input_${session}-cpg.txt";
    my $cpg_output_file = "temp/output_${session}-cpg.txt"; # This file will contain the full CpGProD output
    my $species_flag    = ( $spp eq "Mus musculus" ) ? "-mus" : "";

    open my $cpg_in_fh, '>', $cpg_input_file or warn "Cannot open $cpg_input_file for writing: $!";
    print $cpg_in_fh $seq;
    close $cpg_in_fh;
    chmod 0777, $cpg_input_file;

    my $script_to_call_cpg = "run_cpg_analysis.pl '$cpg_input_file' '$cpg_output_file' '$species_flag' '$session'";
    # CpGProD's output is written to $cpg_output_file by run_cpg_analysis.pl.
    # The STDOUT of run_cpg_analysis.pl only contains the summarized two lines for display.
    my $cpg_summary_out = qx{$^X $script_to_call_cpg};

    # The next line removes a specific message from run_cpg_analysis.pl's STDOUT
    $cpg_summary_out =~ s/^End of the program Bye bye ;-.*\n//mg;
    # This array will only hold the summarized 2 results from run_cpg_analysis.pl's STDOUT
    my @cpg_results_summary = split( /#/, $cpg_summary_out );

    # Now, for the detail button, we will use the full output file directly.

    if ( $? == -1 ) {
        print "Failed to execute script: $!\n";
    }
    elsif ( $? & 127 ) {
        printf "Script died with signal %d, %s coredump\n", ( $? & 127 ), ( $? & 128 ) ? 'including' : 'not including';
    }
    elsif ( $? != 0 ) {
        printf "Script exited with value %d\n", $? >> 8;
    }
    # Return references to summary arrays and the path to the full CpG output file
    return ( \@sigvar, \@covar, \@submotif, \@cpg_results_summary, $cpg_output_file );
}

if ( $input eq "fasta" ) {
    ( $sig_variant, $covariant, $submotifs, $cpg_islands_summary, $cpg_full_file_path ) = connect_motdet( $motif, $pfm, $sequence, $session );
}
elsif ( $input eq "Gene_ID" ) {
    $prom_script = "perl PromoterExtract.pl $idt $genes $up $down $spp $session";
    $prom_seq = qx{$^X $prom_script};
    $prom_seq =~ s/<br>/\n/gi;
    ( $sig_variant, $covariant, $submotifs, $cpg_islands_summary, $cpg_full_file_path ) = connect_motdet( $motif, $pfm, $prom_seq, $session );
}
@sig_variant = @$sig_variant;
@covariant    = @$covariant;
@submotifs    = @$submotifs;
@cpg_islands = @$cpg_islands_summary; # This array holds only the summary results (first 2)

$sv_out1 = $sig_variant[0];
$sv_out2 = $sig_variant[1];

$c_out1 = $covariant[0];
$c_out2 = $covariant[2];

$sm_out1 = $submotifs[0];
$sm_out2 = $submotifs[1];

$cpg_out1 = defined $cpg_islands[0] ? $cpg_islands[0] : "No CpG island result 1";
$cpg_out2 = defined $cpg_islands[1] ? $cpg_islands[1] : "No CpG island result 2";

$sigvar_tsv     = $session . "_significantvariants.tsv";
$sigvar_html    = $session . "_sigvar_html.pl";
$covariants_tsv = $session . "_covariants.tsv";
$submotif_tsv   = $session . "_commonconsensus.tsv";
$cpg_tsv        = $cpg_full_file_path; # Now this points to the full CpGProD output file

print <<HTML;
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Result Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .detail-button {
            background-color: #e5e7eb; /* Gray 200 */
            color: #374151; /* Gray 800 */
            padding: 0.5rem 1rem;
            border-radius: 0.375rem; /* Rounded md */
            font-size: 0.875rem; /* text-sm */
            font-weight: 500; /* font-medium */
            cursor: pointer;
            border: 1px solid #d1d5db; /* Gray 300 */
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* shadow-sm */
            transition: background-color 0.3s ease, transform 0.2s ease; /* Smooth transition */
        }

        .detail-button:hover {
            background-color: #d1d5db; /* Gray 300 on hover */
            transform: scale(1.05); /* Slightly larger on hover */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Add a bit more shadow on hover */
        }

        .detail-button:active {
            transform: scale(0.95); /* Slightly smaller on click */
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05); /* Reduce shadow on click */
        }

        /* Styles for the table */
        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 2rem;
            border: 1px solid #d1d5db; /* Gray 300 */
            border-radius: 0.5rem;
            overflow: hidden; /* to contain rounded corners of thead and tbody */
        }

        .result-table thead {
            background-color: #f3f4f6; /* Gray 100 */
        }

        .result-table th, .result-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #e5e7eb; /* Gray 200 */
        }

        .result-table th {
            font-weight: 600; /* font-semibold */
            color: #4b5563; /* Gray 700 */
        }

        .result-table tbody tr:last-child td {
            border-bottom: none;
        }

        .result-table .detail-cell {
            text-align: center; /* Center the button in the cell */
        }
    </style>
</head>
<body class="bg-#00101a-100 p-6">

    <div class="container mx-auto bg-#071f2c rounded-lg shadow-md p-8">
        <h1 class="text-2xl font-bold text-black-800 mb-6 text-center">Result</h1>
        <div class="space-y-6">
        <form id= "ResultForm">
            <input type = "hidden" name = "fl1"    value = "$sigvar_tsv">
            <input type = "hidden" name = "fl2"    value = "$covariants_tsv">
            <input type = "hidden" name = "fl3"    value = "$submotif_tsv">
            <input type = "hidden" name = "fl4"    value = "$cpg_tsv"> <input type = "hidden" name = "detail_type" id="detail_type" value=""> <table class="result-table">
                <thead>
                    <tr>
                        <th class="text-left">Category</th>
                        <th class="text-left">Description</th>
                        <th class="text-center">Details</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Most significant TFBS & variant</td>
                        <td>
                            <ul class="list-disc list-inside text-black-600">
                                <li>$sv_out1</li>
                                <li>$sv_out2</li>
                            </ul>
                        </td>
                        <td class="detail-cell">
                            <button class="detail-button" type="button" onclick="goToDetails('sigvar')">Details</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Most significant Co-occurring variant</td>
                        <td>
                            <ul class="list-disc list-inside text-black-600">
                                <li>$c_out1</li>
                                <li>$c_out2</li>
                            </ul>
                        </td>
                        <td class="detail-cell">
                            <button class="detail-button" type="button" onclick="goToDetails('covar')">Details</button>
                        </td>
                    </tr>
                    <tr>
                        <td>Most significant Sub-motif</td>
                        <td>
                            <ul class="list-disc list-inside text-black-600">
                                <li>$sm_out1</li>
                                <li>$sm_out2</li>
                            </ul>
                        </td>
                        <td class="detail-cell">
                            <button class="detail-button" type="button" onclick="goToDetails('submotif')">Details</button>
                        </td>
                    </tr>

                    <tr>
                        <td>Most significant CpG Islands</td>
                        <td>
                            <ul class="list-disc list-inside text-black-600">
                                <li>$cpg_out1</li>
                                <li>$cpg_out2</li>
                            </ul>
                        </td>
                        <td class="detail-cell">
                            <button class="detail-button" type="button" onclick="goToDetails('cpg')">Details</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            </form>
        </div>
    </div>

    <script>
        function goToDetails(type){
            const form = document.getElementById("ResultForm");
            // Set the value of the hidden input to indicate which type of details is requested
            document.getElementById("detail_type").value = type;
            form.action = "impat_details.pl"; // Assuming this script handles displaying full results
            form.submit(); // Submit the form
        }
    </script>
</body>
</html>
HTML
