#!/usr/bin/env python3

print("Content-Type: text/html\n")
import cgitb

cgitb.enable()
print("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMPAT - Integrated Mammalian Promoter Analysis Tool</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Framer Motion and React -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/framer-motion/dist/framer-motion.js"></script>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        :root {
            --background: hsl(200, 100%, 5%);
            --foreground: hsl(0, 0%, 98%);
            --card: hsl(200, 70%, 10%);
            --card-foreground: hsl(0, 0%, 98%);
            --primary: hsl(180, 100%, 35%);
            --primary-foreground: hsl(0, 0%, 0%);
            --secondary: hsl(180, 40%, 96%);
            --secondary-foreground: hsl(180, 100%, 20%);
            --muted: hsl(200, 50%, 15%);
            --muted-foreground: hsl(180, 5%, 70%);
            --accent: hsl(164, 100%, 50%);
            --accent-foreground: hsl(0, 0%, 0%);
            --border: hsl(200, 50%, 20%);
            --radius: 0.5rem;
        }

/* Light Theme */
.light-theme {
    --background: hsl(0, 0%, 100%);
    --foreground: hsl(0, 0%, 0%); /* Complete black */
    --card: hsl(165, 100%, 85%);
    --card-foreground: hsl(0, 0%, 0%); /* Complete black */
    --primary: hsl(180, 100%, 35%);
    --primary-foreground: hsl(0, 0%, 100%);
    --secondary: hsl(180, 40%, 96%);
    --secondary-foreground: hsl(180, 100%, 20%); /* You can also adjust this if necessary */
    --muted: hsl(200, 50%, 95%);
    --muted-foreground: hsl(0, 0%, 0%); /* Optional change if used */
    --accent: hsl(164, 100%, 50%);
    --accent-foreground: hsl(0, 0%, 0%);
    --border: hsl(0, 0%, 80%);
}
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--background);
            color: var(--foreground);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        /* Reduce padding in the header */
        .header-gradient {
            background: linear-gradient(to right, rgb(200, 240, 240), rgb(240, 250, 250));
            padding: 0.25rem 1rem; /* Decrease padding */
        }

        .logo {
            height: 60px; /* Increase logo height */
            width: auto; /* Maintain aspect ratio */
        }

        .ibab-logo {
            height: 50px; /* Increase IBAB logo height */
            width: auto; /* Maintain aspect ratio */
        }
        
        .container {
            width: 100%;
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .card {
            background-color: var(--card);
            border-radius: var(--radius);
            border: 1px solid rgba(var(--primary), 0.2);
            backdrop-filter: blur(8px);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: var(--radius);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
            padding: 0.5rem 1rem;
        }
        
        .btn-primary {
            background-color: var(--primary);
            color: var(--primary-foreground);
        }
        
        .btn-primary:hover {
            background-color: hsl(180, 100%, 30%);
        }
        
        .btn-accent {
            background-color: var(--accent);
            color: var(--accent-foreground);
            font-weight: 700;
        }
        
        .btn-accent:hover {
            background-color: hsl(164, 100%, 45%);
        }
        
        .nav-btn {
            display: inline-flex;
            align-items: center;
            padding: 0.625rem 1rem;
            margin: 0.25rem;
            border-radius: var(--radius);
            background-color: var(--primary);
            color: hsl(0, 0%, 0%);
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .nav-btn:hover {
            background-color: hsl(180, 100%, 30%);
        }
        
        .nav-btn svg {
            margin-right: 0.5rem;
        }
        
        .feature-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            padding: 1rem;
            background-color: var(--muted);
            border-radius: var(--radius);
        }
        
        .feature-card svg {
            width: 3rem;
            height: 3rem;
            margin-bottom: 0.5rem;
            color: var(--primary);
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(1, 1fr);
            gap: 1rem;
            margin-top: 1rem;
        }
        
        @media (min-width: 768px) {
            .feature-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        .footer {
            border-top: 1px solid var(--muted-foreground);
            opacity: 0.8;
            margin-top: 3rem;
            padding-top: 1.5rem;
            text-align: center;
            font-size: 0.75rem;
            color: var(--muted-foreground);
        }
        
        /* Animation Classes */
        .animated-fade {
            opacity: 0;
            transform: translateY(20px);
            animation: fadeInUp 0.6s ease forwards;
        }
        
        .staggered-item {
            opacity: 0;
            transform: translateY(20px);
        }
        
        @keyframes fadeInUp {
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .float-animation {
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
            100% {
                transform: translateY(0px);
            }
        }
        
        .delayed-1 {
            animation-delay: 0.1s;
        }
        
        .delayed-2 {
            animation-delay: 0.2s;
        }
        
        .delayed-3 {
            animation-delay: 0.3s;
        }
        
        .delayed-4 {
            animation-delay: 0.4s;
        }
        
        .delayed-5 {
            animation-delay: 0.5s;
        }
        
        /* Transition for buttons */
        .group-hover-translate {
            transition: transform 0.3s ease;
        }
        
        .nav-btn:hover .group-hover-translate {
            transform: translateX(4px);
        }
        
        /* Toggle Switch Styles */
        .toggle-switch {
            display: flex;
            align-items: center;
            cursor: pointer;
        }
        
        .toggle-switch input {
            display: none;
        }
        
        .toggle-switch-label {
            width: 50px;
            height: 24px;
            background-color: var(--primary);
            border-radius: 50px;
            position: relative;
            transition: background-color 0.2s;
        }
        
        .toggle-switch-label::after {
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            width: 20px;
            height: 20px;
            background-color: white;
            border-radius: 50%;
            transition: transform 0.2s;
        }
        
        .toggle-switch input:checked + .toggle-switch-label {
            background-color: hsl(164, 100%, 45%);
        }
        
        .toggle-switch input:checked + .toggle-switch-label::after {
            transform: translateX(26px);
        }
    </style>
</head>
<body>
    <div class="container mx-auto">
    
<!-- Header Section -->
<header class="header-gradient py-0.05 px-4 flex flex-col lg:flex-row items-center justify-between rounded-b-lg animated-fade">
    <div class="flex items-center mb-2 lg:mb-0">
        <!-- Reduced the height of the IMPAT logo -->
        <img src="/IMPAT_logo.png" alt="IMPAT Logo" class="mr-4 float-animation" width="250" height="150">
    </div>
    
    <div class="text-center px-2">
        <h1 class="text-lg md:text-2xl font-bold text-[#01171c]">
            Integrated Mammalian Promoter Analysis Tool
        </h1>
        <p class="italic text-black text-sm md:text-base mt-1">
            (Supported by the Department of Electronics, IT, BT, and S&T, Government of Karnataka)
        </p>
    </div>
    
    <div class="flex items-center">
        <div class="toggle-switch">
            <input type="checkbox" id="theme-toggle">
            <label class="toggle-switch-label" for="theme-toggle"></label>
        </div>
        <img src="/IBAB_logo.png" alt="IBAB Logo" class="h-10 w-auto md:h-10 transition-transform hover:scale-110 ml-4">
    </div>
</header>

        
<!-- Navigation -->
<nav class="my-6 flex flex-wrap justify-center gap-2 px-4">
    <button class="nav-btn staggered-item animated-fade delayed-1" onclick="showContent('home')">
        <i data-lucide="home" width="16" height="16"></i>
        Home
    </button>
    <button class="nav-btn staggered-item animated-fade delayed-2" onclick="showContent('guide')">
        <i data-lucide="book-open" width="16" height="16"></i>
        User Guide
    </button>
    <button class="nav-btn staggered-item animated-fade delayed-3" onclick="showContent('publication')">
        <i data-lucide="file-text" width="16" height="16"></i>
        Publication
    </button>
    <button class="nav-btn staggered-item animated-fade delayed-4" onclick="showContent('contact')">
        <i data-lucide="mail" width="16" height="16"></i>
        Contact
    </button>
    <button class="nav-btn staggered-item animated-fade delayed-5" onclick="showContent('help')">
        <i data-lucide="help-circle" width="16" height="16"></i>
        Help
    </button>
</nav>

<!-- Content Area -->
<div id="content-area" class="text-center mt-6 px-4">
    <div id="home" class="hidden">Welcome to the Home Page!</div>
    <div id="guide" class="hidden">Here is the User Guide content.</div>
    <div id="publication" class="hidden">Explore our Publications here.</div>
    <div id="contact" class="hidden">Get in touch with us via Contact page.</div>
    <div id="help" class="hidden">Need Help? You're in the right place!</div>
</div>

<!-- Script -->
<script>
    function showContent(id) {
        const sections = ['home', 'guide', 'publication', 'contact', 'help'];
        sections.forEach(section => {
            document.getElementById(section).classList.add('hidden');
        });
        document.getElementById(id).classList.remove('hidden');
    }
</script>

<!-- Start Analysis Dropdown -->
<div class="flex justify-center mt-4">
    <div class="relative inline-block text-left">
        <div>
            <button type="button" class="btn btn-accent py-4 px-6 text-lg group" id="dropdownButton">
                <span>Start Analysis</span>
                <i data-lucide="chevron-right" class="ml-2 group-hover-translate"></i>
            </button>
        </div>

<!-- Dropdown Menu -->
        <div id="dropdownMenu" class="absolute right-0 z-10 hidden mt-2 w-60 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-10">
            <div class="py-1" role="menu" aria-orientation="vertical" aria-labelledby="dropdownButton">
                <a href="impat_index.py?option=fasta" class="block px-4 py-2 text-sm text-black hover:bg-gray-100 whitespace-nowrap" role="menuitem">Promoter sequence</a>
                <a href="impat_index.py?option=Gene_ID" class="block px-4 py-2 text-sm text-black hover:bg-gray-100 whitespace-nowrap" role="menuitem">GENE/ENSEMBLE ID</a>
                <a href="impat_index.py?option=tissue" class="block px-4 py-2 text-sm text-black hover:bg-gray-100 whitespace-nowrap" role="menuitem">Tissue/Condition</a>
            </div>
        </div>
    </div>
</div>

<!-- Tailwind Utility -->
<style>
    .hidden {
        display: none;
    }
</style>

        
        <!-- Main Content Section -->
        <main class="w-full max-w-6xl mx-auto px-4 py-8">
            <div class="space-y-8">
                <!-- Intro Card -->
                <div class="card animated-fade delayed-1">
                    <div class="pt-6">
                        <p class="text-lg leading-relaxed">
                            IMPAT is a powerful in silico tool designed for comprehensive analysis and prediction of mammalian promoters. 
                            It helps researchers uncover key regulatory features influencing gene expression by analyzing promoter sequences 
                            of co-expressed genes.
                        </p>
                    </div>
                </div>
                
                <!-- Why Use Card -->
                <div class="card animated-fade delayed-2">
                    <div class="p-6">
                        <h2 class="text-2xl font-bold mb-4" style="color: #00997A;">Why Use IMPAT?</h2>
                        <div class="space-y-4">
                            <p class="leading-relaxed">
                                Gene regulation in mammals is highly complex, involving multiple regulatory elements like transcription 
                                factor binding sites (TFBSs), CpG islands, motif variations, repeat elements, alternatively spliced isoforms, 
                                and DNA structural features. Existing promoter analysis tools focus primarily on TFBSs, limiting insights into gene regulation.
                            </p>
                            <p class="leading-relaxed">
                                IMPAT integrates multiple analysis modules to provide a holistic view of promoter characteristics.
                            </p>
                        </div>
                    </div>
                </div>
                
                <!-- Features Card -->
                <div class="card animated-fade delayed-3">
                    <div class="p-6">
                        <h2 class="text-xl text-accent font-bold mb-4">Key Features</h2>
                        <div class="feature-grid">
                            <div class="feature-card">
                                <i data-lucide="flask-conical" width="48" height="48"></i>
                                <h3 class="text-lg font-medium mb-2">Comprehensive Analysis</h3>
                                <p class="text-sm text-muted-foreground">Analyze multiple regulatory features in one go</p>
                            </div>
                            
                            <div class="feature-card">
                                <i data-lucide="dna" width="48" height="48"></i>
                                <h3 class="text-lg font-medium mb-2">Sequence Insights</h3>
                                <p class="text-sm text-muted-foreground">Identify regulatory motifs across mammalian genomes</p>
                            </div>
                            
                            <div class="feature-card">
                                <i data-lucide="microscope" width="48" height="48"></i>
                                <h3 class="text-lg font-medium mb-2">Predictive Power</h3>
                                <p class="text-sm text-muted-foreground">Predict promoter activity in novel sequences</p>
                            </div>
                        </div>
                        <div class="mt-4 text-center w-full text-muted-foreground">
                            <p>IMPAT is a one-stop solution for scientists looking to characterize promoters, identify regulatory motifs, and 
                            predict promoter activity in novel sequences.</p>
                        </div>
                    </div>
                </div>
        
        <!-- Footer -->
        <footer class="footer">
            <div class="max-w-6xl mx-auto px-4 py-4 text-center">
                <p class="text-sm text-muted-foreground">
                    © copyright 2023, All rights reserved; contact kshithish@ibab.ac.in
                </p>
                <p class="text-xs text-muted-foreground mt-2">
                    Disclaimer: The purpose of this server is to assist in scientific community discoveries. 
                    We cannot, however, guarantee that there will be no inaccuracies.
                </p>
            </div>
        </footer>
    </div>
    
    <!-- Initialize Lucide Icons -->
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        lucide.createIcons();
        
        // Add staggered animation to navigation buttons
        const staggeredItems = document.querySelectorAll('.staggered-item');
        staggeredItems.forEach((item, index) => {
            setTimeout(() => {
                item.classList.add('animated-fade');
            }, 100 * index);
        });

        // Dropdown functionality
        const dropdownButton = document.getElementById('dropdownButton');
        const dropdownMenu = document.getElementById('dropdownMenu');

        dropdownButton.addEventListener('click', () => {
            dropdownMenu.classList.toggle('hidden');
        });

        // Close dropdown if clicked outside
        window.addEventListener('click', (event) => {
            if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
                dropdownMenu.classList.add('hidden');
            }
        });

        // Theme toggle functionality
        const themeToggle = document.getElementById('theme-toggle');
        themeToggle.addEventListener('change', function() {
            document.body.classList.toggle('light-theme', this.checked);
        });
    });
    
        document.addEventListener('DOMContentLoaded', function() {
            lucide.createIcons();
            
            // Add staggered animation to navigation buttons
            const staggeredItems = document.querySelectorAll('.staggered-item');
            staggeredItems.forEach((item, index) => {
                setTimeout(() => {
                    item.classList.add('animated-fade');
                }, 100 * index);
            });

            // Theme toggle functionality
            const themeToggle = document.getElementById('theme-toggle');
            themeToggle.addEventListener('change', function() {
                document.body.classList.toggle('light-theme', this.checked);
            });
        });
    </script>
</body>
</html>
""")
