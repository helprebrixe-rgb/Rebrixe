// Google Analytics
const _gaScript = document.createElement('script');
_gaScript.async = true;
_gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-WXNSZGYWXW';
document.head.appendChild(_gaScript);

window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-WXNSZGYWXW');


/* Rebrixe OMNI-NAV - Master Controller (RESTORED PRESET) */

const categories = {
        "growth": ["Affiliate Link Disclosure Gen","Ai Text Humanizer","Backlink ROI Calculator","Bio Generator","Bio Optimizer","Brand Deal Estimator","Brand Voice Consistency Checker","Bulk Mention Cleaner", "Caption Pro","Carousel Slide Counter","Click Worth Calculator","Color Palette Extractor","Comment Art Vault","Content Boredom Breaker","Content Velocity Modeler","CPM Calculator","Dark Mode Logo Tester","Emoji String Generator","Favicon Previewer","Giveaway Rule Generator", "Grid Previewer", "Hashtag Stacker","Hashtag to Keyword Converter", "Insta Caption Crafter","Insta Invisible Spacer","Instagram Safe Zone Overlay","Influencer Red Flag Checklist","Json LD Rich Snippet Architect","Keyword KEI Checker",
            "LinkedIn Authority Generator","LinkedIn Line Breaker","Media Kit Generator","Niche Mapper","OG Preview Simulator","Organic Traffic Lead Value Modeler","PFP Glow Ring","PFP Previewer","Pinterest Ratio Validator","Pinterest Description Generator", "Podcast Blurb Generator","Podcast Segmenter","Portrait Letterboxer","Post to Reel Planner","Power Word Inserter","Profile QR Code Gen","pSEO Matrix","Repurposing Matrix","Retention Script Map","Reverse Text Generator","Safe Zone Checker", "Script Timer","Script to Shorts Prompt Generator","SEO Silo Map Generator","Shorts Safe Zone Checker","Slug Validator","Social Meta Card Simulator","Social Share Link Gen","Story Background Blur Gen","Subject Line AB Tester","Text Art Vault",
            "Text on Video Contrast Checker","Thumbnail Previewer","Thumbnail Squint Test","Tik Tok Viral Prob","TikTok Hook Generator","TikTok Safe Zone Overlay","Tweet Thread Starter","UGC Script Builder","Universal Aspect Ratio Converter","UTM Builder","Vibe Text Gen","Video Script Intros","Viral Hook Generator","Viral Storyline Builder","Watermark Positioner","YouTube Thumbnail Red Bar Simulator","YouTube Timestamp Formatter", "YouTube Title Case Converter"],
        
        "technical": ["Anchor Text and Link Extractor","Aspect Ratio and CLS Calculator","Audit Checklist", "Base64 Studio","Base64 to Image","Binary to Text","Browser User Agent Parser","Bulk String Case Converter","Bulk URL Slug Gen","Bulk UUID Guild V4 Generator","Canonical Tag Generator","Chmod Calculator","Clamp Typography Builder","Code and Text Diff Checker","Color Converter","CORS Header Generator","Crontab Expression Builder","CSP Generator","CSS Box Shadow Builder","CSS Flexbox Playground","CSS Glassmorphism Builder","CSS Grid Template Area Builder","CSS Keyframe Animation Builder","CSS Minifier","CSV to JSON","Dev Stopwatch and Millisecond Timer","Dockerfile Boilerplate Generator","EM to PX Calculator",
            "Epoch and Unix Timestamp Converter","Fancy Border Radius Visualizer","Git Command Wizard","GitHub ReadMe Builder","GitIgnore Generator","Golden Ratio Layout Engine","Gradient Gen","Heading Hierarchy Analyzer","HEX to ASCII Converter","Hreflang Tag Generator","Htaccess Builder","Html Entity Studio","HTML Minifier","HTML Stripper","HTML Tag Checker and Auto Closer","Image to Base64","Javascript Keycode Detector","JS Minifier","JSON Formatter","JSON LD Data Validator and Template","JSON to CSV","JSON Validator and Linter","JWT Decoder","Keyword Density Checker","Lorem Ipsum","MailTo Link Builder", "Markdown Converter", "Meta Tag Gen", "Mobile Tester","Nginx Proxy and Redirect Wizard","OG Tag Previewer and Gen",
            "Password and Hash Generator","PWA Manifest Builder", "Px to Rem Converter","Redirect Generator","Regex Match Extractor","Regex Sandbox and Cheat sheet","Robots File Tester", "Robots Generator", "Schema Generator","SemVer Calculator","SERP Simulator","Service Worker Generator","Shell Script Boilerplate Gen","SQL Query Formatter","SQL Schema Builder","SVG Optimizer and Minifier","SVG to Data URI Converter","Tailwind CSS Class Explainer","Text Sorter and Duplicator","Twitter Card Previewer and Generator","UI Color Palette Generator","URL Decoder","URL Encoder","URL Parameter Stripper and Parser","Viewport and Breakpoint Tester","VS Code Snippet Builder","WCAG Color Contrast Checker","Web Security Headers Builder"
            ,"Word Counter","XML Formatter and Beautifier", "XML Sitemap Generator"],
        
        "generators": ["Aesthetic Username generator","Agency Name Generator","alias and persona generator","Anime Attack Name Gen","App Name Generator","Bakery Brand Namer","Cafe Name Generator","Call of Duty Regiment Gen","Car Nickname Gen","Clan name generator","clothing brand namer","Cocktail or Drink Namer","Consultancy Firm Namer","Cosplay Stage Namer","Cottagecore Name Gen","Cozy Farm and Town Namer","Cryptocurrency Namer","Cyberpunk City Namer","Cult Namer","Dark Academia Persona Namer","discord server namer","DnD Tavern Namer","Dystopian Megacorp Namer","E Boy Alias Gen","E Girl Alias Gen","Eco Friendly Brand Namer","Empire Name Generator","Etsy Name Generator","Fantasy name generator","Farm and Homestead Namer",
            "Finsta Generator","Fleet and Armada Namer","French Shop Namer","Furniture Brand Gen","Gamer Name generator","Gender Neutral Name Gen","Gothic Victorian Name Gen","Grimoire or Spellbook Namer","Gym Name Generator","Hotel and Resort Namer","House Name Generator","Italian Fashion Brand Namer","Japanese Business Namer","Jewelry Brand Namer","Kingdom Name Generator","Korean Skincare Namer","Kpop Stage Name Generator","Latin Root Brand Namer","Legal Firm Namer","LLM Startup Namer","Magical School Namer","Mech and Pilot Callsign Gen","Minecraft Server Name Gen","Mythical Creature Namer","Noir Detective Agency Namer","Old Money Aesthetic Namer","Perfume Brand Namer","Pet Name generator",
            "Pirate Ship and Crew Gen","Plant Name Generator","podcast name generator","Post Apocalyptic Faction Gen","Project Codename Generator","Real Estate Team Namer","Recipe Namer","Roblox Group Namer","SaaS Name Generator","Sci Fi Planet Namer","Shopify Store Namer","Side Hustle Handle","Smurf Name Generator","Spaceship Name Generator","Starwars OC Namer","Steam Group and Library Namer","Steampunk Airship Namer","Substack Newsletter Namer","Supervillain Moniker Gen","Team Building Group Namer","Twin Baby Name Matcher","Twitch Stream Namer","Twitch Team Namer", "Valorant Agent Nicknames Gen" ,"VR Chat Persona Gen" , "Vtuber Name Generator","Webtoon and Manhwa Title Gen","Wifi Network Namer","Yacht Namer"],

        "image-visual": ["Add Text to Image","Add White Background to PNG","Aspect Ratio Calculator","Aspect Ratio Cropper","Average Color Calculator","Background Blur Tool","Background Color Overlay","Background Pattern Adder","Batch Watermark Tool","BMP to JPG Converter","Brand Color Extractor","Brightness Contrast Adjuster","Bulk EXIF Viewer","Bulk Format Converter","Bulk Image Compressor","Bulk Image Resizer","Camera Settings Reader","Canvas Size Expander","Change Background Color","Circle Image Cropper","Collage Maker","Color Accessibility Checker","Color Balance Tool","Color Palette Extractor","Color Picker from Image","Color Replace Tool","Copyright Stamp Tool","Custom Shape Cropper","Dominant Color Finder",
            "Duotone Image Generator","Exact File Size Resizer","EXIF Data Viewer","Exposure and Gamma Corrector","Fake Image Detector","Favicon Generator Pack","GIF Compressor","GIF Cropper","GIF Frame Viewer","GIF Frames Extractor","GIF Resizer","GIF Speed Changer","GIF Text Adder","GIF to PNG Converter","Gradient Image Generator","Grid Cropper","HEIC to JPG Converter","Hue Rotation Tool","Image Blur Tool","Image Caption Adder","Image Comparison Tool","Image Compressor and Comparer","Image Cropper","Image Dimension Checker","Image DPI Changer","Image File Info Tool","Image Filter Pack","Image Flipper","Image Grid Splitter","Image Info Inspector","Image Metadata Stripper","Image Noise Reducer","Image Padding Adder",
            "Image Resizer by Pixels","Image Resizer without Stretching","Image Rotator","Image Size Reducer","Image Straightener","Image Tiler","Image to CSS Gradient","Image to Greyscale Converter","Image to WebP Converter","Image Watermark Tool","Images to GIF Animator","Invert Image Colors","JPEG Compressor","JPEG to WEBP Converter","JPG to PNG Converter","Meme Generator","Multi Image Stitcher","Pattern Generator","Perspective Corrector","Photo Privacy Auditor","Placeholder Image Generator","PNG Compressor","PNG to JPG Converter","PNG to WebP Converter","Print Size Calculator","QR Generator with Logo","Quote Card Maker","Ratio Crop Tool","Saturation Vibrance Tool","Screenshot Mockup Generator","Sepia Filter Tool","Sharpen Image Tool",
            "Smart Batch Image Converter","Social Media Banner Generator","Social Media Image Resizer","Solid Background Remover","Solid Color Image Generator","Square Image Maker","SVG Compressor","Text Watermark Generator","Text Watermark Overlay","Thumbnail Resizer","WebP Compressor","WebP to JPG Converter","White Background Remover","White Balance Corrector"],
        
        "time-date": ["12 to 24 Hour Converter","24 to 12 Hour Converter","Academic Year Calculator","Add Subtract Days","Age at Date Calculator","Age Calculator","Bi Weekly Pay Calculator","Billable Hours Tracker","Break Reminder Timer","Break Time Calculator","Bulk Date Format Converter","Business Days Calculator","Call Scheduler Across Time Zones","Chess Clock and Debate Timer","Class Schedule Builder","Content Calendar Generator","Contractor Day Rate Calculator","Current Time in Any City","Daily Hours Logger","Daily Routine Builder","Date Difference Breakdown","Date Format Converter","Date Range Generator","Day of Week Finder","Days Between Dates Calculator","Days in Month Calculator","Days Since Calculator","Days Until Calculator",
            "Deadline in My Timezone","Deadline Probability Tool","Decimal to Time Converter","Deep Work Session Planner","DST Dates Checker","DST Meeting Impact Tracker","Editorial Calendar Planner","Epoch Time Calculator","Event Countdown","First and Last Day of Month","Fiscal Year Calculator","Flight Time Zone Adjuster","Focus Session Tracker","Freelance Project Profitability Calculator","Habit Streak Tracker","Holiday Date Calculator","Hourly to Salary Converter","Hours and Minutes Calculator","Hours to Minutes Converter","Interval Timer","Invoice Hours Calculator","ISO 8601 Date Converter","Leap Year Checker","Loan Subscription End Date Calculator","Lunch Break Deduction Tool","Meeting Time Overlap Finder",
            "Meeting Timer","Minutes to Hours Converter","Month Calculator","Multi Date Event Planner","Next Weekday Finder","OnCall Schedule Generator","Online Countdown Timer","Overnight Shift Calculator","Overtime Calculator","Pay per Hour Calculator","Pomodoro Timer","Pregnancy Due Date Calculator","Presentation Timer","Printable Monthly Calendar","Printable Yearly Calendar","Productive Hours Analyser","Project Timeline Calculator","Quarter Dates Calculator","Recurring Date Generator","Recurring Meeting Time Finder","Retainer Hours Tracker","Salary to Hourly Converter","School Year Planner","Seconds to Minutes Converter","Shift Pay Calculator","Shift Rotation Calendar","Shift Start Time Planner","Social Media Posting Schedule Gen",
            "Spoken Time Converter","Sprint Planning Calendar","Stopwatch","Study Session Timer","Team Availability Heatmap","Time Addition Calculator","Time Block Planner","Time Rounding Calculator","Time to Decimal Converter","Time to Percent of the day","Time Zone Abbreviation Lookup","Time Zone Converter","Time Zone Difference Calculator","Timesheet Generator","Unix Timestamp Converter","UTC Offset Lookup","Video Runtime Calculator","Webinar Time Converter","Week NUmber Calculator","Weekdays Counter","Weekend Days Counter","Weekly Timesheet Calculator","Work Anniversary Calculator","Working Days in Month","World Clock Dashboard"]
        
    };

const toolLibrary = [];
Object.keys(categories).forEach(folder => {
    categories[folder].forEach(name => {
        const slug = name.toLowerCase().replace(/ /g, "-") + ".html";
        toolLibrary.push({ name: name, link: `/${folder}/${slug}`, folder: folder });
    });
});

const globalUI = `
<style>
/* 1. RESTORED HEADER & LOGO ANIMATIONS */
.tf-header { 
    display: flex;
justify-content: space-between;
align-items: center;
padding: 10px 20px;
width: 100%;
box-sizing: border-box;

/* Glass replacement for background: #05070a */
background: rgba(5, 7, 10, 0.45);
backdrop-filter: blur(20px) saturate(180%);
-webkit-backdrop-filter: blur(20px) saturate(180%);

/* Upgraded border */
border-bottom: 1px solid rgba(255, 255, 255, 0.08);
box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.06),
    0 4px 24px rgba(0, 0, 0, 0.3);

position: sticky;
top: 0;
z-index: 9999;
transition: transform 0.5s ease-in-out;
}
.tf-header.nav-hidden { transform: translateY(-100%); }

.logo { 
    font-family: 'Outfit'; font-size: 1.2rem; font-weight: 800; 
    background: linear-gradient(135deg, #ffffff 30%, var(--primary) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-decoration: none; letter-spacing: -1px; flex-shrink: 0;
}
.logo:hover { 
    background: linear-gradient(90deg, #00f2fe, var(--primary), #4facfe);
    background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: tf-shine 1.5s linear infinite;
    filter: drop-shadow(0 0 12px var(--primary)); transform: scale(1.02);
}
@keyframes tf-shine { to { background-position: 200% center; } }

/* 2. THE STEALTH SEARCH BOX */
#searchWrapper { position: relative; width: 100%; max-width: 250px; height: 36px; z-index: 10000; }
#toolSearch { 
    width: 100%; height: 100%; background: rgba(255, 255, 255, 0.05); 
    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 50px; 
    color: #f1f5f9; padding: 0 10px 0 35px; font-size: 0.85rem; outline: none; box-sizing: border-box;
    transition: box-shadow 0.4s ease, border-color 0.2s ease, background 0.2s ease;
}
#toolSearch:focus { 
    border-color: var(--primary); background: #000; 
    box-shadow: 0 0 20px -5px var(--primary);
}
#searchWrapper::before {
    content: ""; position: absolute; left: 14px; top: 50%; transform: translateY(-50%);
    width: 14px; height: 14px;
    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>') no-repeat center;
    opacity: 0.4; filter: drop-shadow(0 0 2px var(--primary)); pointer-events: none;
}

/* 3. PREMIUM RESULTS DROPDOWN */
#searchResults { 
    position: absolute; top: calc(100% + 8px); left: 0; right: 0; 
    background: #05070a; border: 1px solid #1e293b; border-radius: 20px; 
    max-height: 450px; overflow-y: auto; display: none; 
    box-shadow: 0 20px 40px rgba(0,0,0,0.6); z-index: 10001;
    animation: premiumFade 0.5s ease-out;
}
@keyframes premiumFade { from { opacity: 0; transform: translateY(-5px); } to { opacity: 1; transform: translateY(0); } }

.search-item { 
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 20px; text-decoration: none; border-bottom: 1px solid #0f172a; transition: 0.2s;
}
.search-item:hover { background: #0f172a; }
.search-item b { color: #f1f5f9; font-size: 0.9rem; font-weight: 500; }
.search-item span { color: var(--primary); font-size: 0.6rem; text-transform: uppercase; font-weight: 900; }

/* 4. MOBILE SHIT-FIXER */
@media (max-width: 600px) {
    .tf-header { padding: 10px 15px; flex-direction: row !important; }
    .logo { font-size: 1.1rem; }
    #searchWrapper { max-width: 160px; }
}
    /* 5. MASTER BACK BUTTON */
/* 5. MASTER SPLIT-NAV CONTROLLER */
.back-btn-wrapper { 
    display: flex;
    justify-content: space-between; /* This pushes them to the sides */
    align-items: center;
    margin: 20px 0 30px 0; 
    width: 100%;
}

.nav-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #94a3b8;
    text-decoration: none;
    font-size: 0.75rem;
    font-weight: 800;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Left Button (Hub) Hover */
.nav-link.left-nav:hover {
    color: var(--primary);
    background: rgba(255, 255, 255, 0.07);
    border-color: var(--primary);
    transform: translateX(-5px);
}

/* Right Button (Home) Hover */
.nav-link.right-nav:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
}

.nav-link svg {
    width: 14px;
    height: 14px;
    stroke-width: 3px;
}
    /* OMNI-NAV SPLIT SYSTEM */
.omni-nav-bar { 
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    width: 100%;
    pointer-events: auto;
}

.omni-link {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #64748b;
    text-decoration: none;
    font-size: 0.7rem;
    font-weight: 800;
    transition: all 0.2s ease;
    padding: 8px 14px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.omni-link:hover {
    color: var(--primary);
    background: rgba(255, 255, 255, 0.06);
    border-color: var(--primary);
}

.omni-link svg { width: 14px; height: 14px; stroke-width: 2.5px; }

/* Right side specific hover */
.omni-home:hover { transform: translateX(3px); color: #fff; }
.omni-hub:hover { transform: translateX(-3px); }
</style>

<header class="tf-header">
    <a href="/" class="logo">Rebrixe</a>
    <div id="searchWrapper">
        <input type="text" id="toolSearch" placeholder="Search..." autocomplete="off">
        <div id="searchResults"></div>
    </div>
</header>`;

const footerUI = `
<footer class="tf-footer">
    <div class="footer-content" style="display: flex; justify-content: space-between; padding: 40px 20px; max-width: 1200px; margin: 0 auto; flex-wrap: wrap; gap: 30px;">
        <div>
            <h3 style="color:var(--primary); font-family:'Outfit'; margin-bottom: 10px;">Rebrixe</h3>
            <p style="opacity: 0.7; font-size: 0.9rem;">The web’s fastest utility engine. Built for performance.</p>
        </div>
        <div>
            <h4 style="color:#fff; margin-bottom: 10px;">Platform</h4>
            <p><a href="/privacy.html" style="color:inherit; text-decoration:none; opacity: 0.7;">Privacy Policy</a></p>
            <p><a href="/terms.html" style="color:inherit; text-decoration:none; opacity: 0.7;">Terms of Service</a></p>
            <p><a href="/about-us.html" style="color:inherit; text-decoration:none; opacity: 0.7;">About Us</a></p>
            <p><a href="/faq.html" style="color:inherit; text-decoration:none; opacity: 0.7;">FAQ</a></p>
        </div>
        <div>
            <h4 style="color:#fff; margin-bottom: 10px;">Contact</h4>
            <p><a href="mailto:help.rebrixe@gmail.com" style="color:var(--primary); text-decoration:none; font-weight: 700;">help.rebrixe@gmail.com</a></p>
        </div>
    </div>
    <div class="footer-bottom" style="text-align: center; padding: 20px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 0.75rem; opacity: 0.5;">© 2026 Rebrixe Engine. All processing is 100% Client-Side.</div>
</footer>`;


const seoUI = `
<section class="seo-authority-section" style="max-width: 1000px; margin: 100px auto 40px; padding: 60px 20px; border-top: 1px solid #1e293b; color: #94a3b8; line-height: 1.8; font-size: 0.95rem;">
    
    <div style="margin-bottom: 50px;">
        <h2 style="font-family: 'Outfit'; color: #fff; font-size: 2.2rem; margin-bottom: 25px; letter-spacing: -1px;">
            The Architecture of <span style="color: var(--primary);">High-Performance Web Utilities</span>
        </h2>
        <p style="font-size: 1.1rem; color: #cbd5e1; margin-bottom: 20px;">
            In the modern digital landscape, the tools we use define the speed of our innovation. <strong>Rebrixe</strong> was conceived as a response to the bloated, ad-heavy utility sites of the past decade. We provide a streamlined, <strong>privacy-centric infrastructure</strong> for developers, digital marketers, and creative entrepreneurs who require precision without compromise.
        </p>
        <p>
            Unlike traditional platforms that rely on server-side processing—which introduces latency and potential security vulnerabilities—the Rebrixe engine operates on a <strong>decentralized execution model</strong>. By leveraging the power of modern browser APIs and ES6+ JavaScript, every calculation, formatting task, and generation happens locally on your hardware. This "Client-Side First" philosophy ensures that your sensitive data—from proprietary source code to brand-new startup identities—never leaves the safety of your local environment.
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 40px; margin-bottom: 50px;">
        <div>
            <h3 style="font-family: 'Outfit'; color: var(--primary); font-size: 1.3rem; margin-bottom: 15px;">Why Data Sovereignty Matters</h3>
            <p style="font-size: 0.9rem;">
                Every time you paste code or text into a standard online tool, you risk your data being logged, analyzed, or sold. Rebrixe eliminates this risk entirely. Our <strong>Zero-Log Policy</strong> isn't just a promise; it's a technical reality enforced by our architecture. Because there is no back-end database receiving your inputs, your intellectual property remains 100% yours. This makes Rebrixe the gold standard for enterprise-level developers and privacy-conscious creators.
            </p>
        </div>
        <div>
            <h3 style="font-family: 'Outfit'; color: var(--primary); font-size: 1.3rem; margin-bottom: 15px;">Optimized for Digital Agility</h3>
            <p style="font-size: 0.9rem;">
                Speed is the ultimate feature. By stripping away heavy frameworks and tracking scripts, we’ve achieved <strong>near-instantaneous load times</strong>. Our tools are designed with a "Gen Z" aesthetic—minimalist, high-contrast, and mobile-responsive—ensuring that your workflow isn't interrupted, whether you're at a desktop workstation or optimizing on the go. Rebrixe isn't just a website; it's a productivity multiplier designed for the fast-paced 2026 web ecosystem.
            </p>
        </div>
    </div>

    <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid #1e293b; padding: 40px; border-radius: 24px; margin-bottom: 40px;">
        <h3 style="font-family: 'Outfit'; color: #fff; margin-bottom: 20px; font-size: 1.4rem;">The Rebrixe Technical Edge</h3>
        <p style="margin-bottom: 20px; font-size: 0.9rem;">
            Our suite is divided into three specialized hubs to cater to every facet of the digital journey:
        </p>
<ul style="list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 16px; font-size: 0.85rem;">
            <li style="display: flex; flex-direction: column; gap: 5px; min-width: 0;">
                <strong style="color: var(--primary);">Technical Hub:</strong>
                <span>Advanced JSON formatting, CSS minification, and SEO audit tools for hardened workflows.</span>
            </li>
            <li style="display: flex; flex-direction: column; gap: 5px; min-width: 0;">
                <strong style="color: var(--primary);">Growth Hub:</strong>
                <span>Social content generators, engagement calculators, and viral hook engines.</span>
            </li>
            <li style="display: flex; flex-direction: column; gap: 5px; min-width: 0;">
                <strong style="color: var(--primary);">Generator Hub:</strong>
                <span>AI naming utilities for SaaS startups, personas, and brand identities.</span>
            </li>
            <li style="display: flex; flex-direction: column; gap: 5px; min-width: 0;">
                <strong style="color: var(--primary);">Visual Hub:</strong>
                <span>Image compressors, resizers, optimizers, croppers, and watermark tools.</span>
            </li>
            <li style="display: flex; flex-direction: column; gap: 5px; min-width: 0;">
                <strong style="color: var(--primary);">Time Hub:</strong>
                <span>Converters, calculators, stopwatches, world clocks, and calendar utilities.</span>
            </li>
        </ul>
    </div>

    <p style="text-align: center; color: #475569; font-size: 0.85rem; max-width: 700px; margin: 0 auto;">
        By choosing Rebrixe, you are supporting a faster, more private, and more beautiful internet. We are constantly expanding our library of tools to meet the evolving needs of the global creator community. 
        <strong>100% Free. 100% Secure. 100% Client-Side.</strong>
    </p>

</section>`;


function initRebrixe() {
    // 1. Header & Footer Injection
    const navContainer = document.querySelector('.nav-container') || document.querySelector('header');
    if (navContainer) navContainer.innerHTML = globalUI;

    const footerTag = document.querySelector('footer');
    if (footerTag) footerTag.innerHTML = footerUI;

    // 2. SEO SECTION INJECTION (The big text block)
    if (footerTag) {
        footerTag.insertAdjacentHTML('beforebegin', seoUI);
    }

    // 3. META TAG INJECTION (The "Invisible" SEO)
    injectSmartSEO();

    // 2. SAFE SPLIT-NAV INJECTION
    const container = document.querySelector('.container');
    if (container) {
        // Remove ONLY the omni-nav if it already exists (prevents duplicates)
        const existingNav = document.getElementById('omni-nav-trigger');
        if (existingNav) existingNav.remove();

        const path = window.location.pathname;
       
        // Replace the old hubDest logic with this:
        if (path !== "/" && path !== "/index.html" && path.length > 1) {
let hubDest = "/"; // Default to root
let hubLabel = "All Tools";

if (path.includes('/growth/')) { hubDest = "/growth/"; hubLabel = "Growth Hub"; }
else if (path.includes('/technical/')) { hubDest = "/technical/"; hubLabel = "Technical Hub"; }
else if (path.includes('/generators/')) { hubDest = "/generators/"; hubLabel = "Generator Hub"; }
else if (path.includes('/image-visual/')) { hubDest = "/image-visual/"; hubLabel = "Image-Visual Hub"; }
else if (path.includes('/time-date/')) { hubDest = "/time-date/"; hubLabel = "Time-Date Hub"; }


            const splitNavHTML = `
                <div id="omni-nav-trigger" class="omni-nav-bar">
                    <a href="${hubDest}" class="omni-link omni-hub">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
                        <span>${hubLabel}</span>
                    </a>
                    <a href="/" class="omni-link omni-home">
                        <span>Home</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
                    </a>
                </div>
            `;
            // Insert at the top of the container
            container.insertAdjacentHTML('afterbegin', splitNavHTML);
        }
    }

    setupSearchLogic();
    setupSmartHeader();
}

function setupSmartHeader() {
    const header = document.querySelector('.tf-header');
    let lastScrollY = window.scrollY;
    window.addEventListener("scroll", () => {
        if (!header) return;
        const currentScrollY = window.scrollY;
        if (currentScrollY > lastScrollY && currentScrollY > 80) {
            header.classList.add("nav-hidden");
        } else {
            header.classList.remove("nav-hidden");
        }
        lastScrollY = currentScrollY;
    });
}

function setupSearchLogic() {
    const input = document.getElementById('toolSearch');
    const results = document.getElementById('searchResults');
    const contentToFade = document.querySelector('.tool-wrapper') || document.querySelector('.tool-card');

    if(!input) return;
    input.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase().trim();
        if (term.length > 0) {
            const matches = toolLibrary.filter(t => {
                const name = t.name.toLowerCase();
                return name.includes(term) || getFuzzyMatch(term, name.substring(0, term.length + 3)) <= 3;
            }).slice(0, 8);

            results.innerHTML = matches.length > 0 ? 
                matches.map(t => `<a href="${t.link}" class="search-item"><b>${t.name}</b><span>${t.folder} →</span></a>`).join('') :
                `<div style="padding:20px; text-align:center">No tools found</div>`;
            
            results.style.display = 'block';
            if(contentToFade) contentToFade.style.opacity = "0.2";
        } else {
            results.style.display = 'none';
            if(contentToFade) contentToFade.style.opacity = "1";
        }
    });

    document.addEventListener('click', (e) => {
        const wrapper = document.getElementById('searchWrapper');
        if (wrapper && !wrapper.contains(e.target)) {
            results.style.display = 'none';
            if(contentToFade) contentToFade.style.opacity = "1";
        }
    });
}

function getFuzzyMatch(s1, s2) {
    s1 = s1.toLowerCase(); s2 = s2.toLowerCase();
    let costs = new Array();
    for (let i = 0; i <= s1.length; i++) {
        let lastValue = i;
        for (let j = 0; j <= s2.length; j++) {
            if (i == 0) costs[j] = j;
            else if (j > 0) {
                let newValue = costs[j - 1];
                if (s1.charAt(i - 1) != s2.charAt(j - 1))
                    newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
                costs[j - 1] = lastValue;
                lastValue = newValue;
            }
        }
        if (i > 0) costs[s2.length] = lastValue;
    }
    return costs[s2.length];
}

function injectSmartSEO() {
    const pageTitle = document.title;
    const currentUrl = window.location.href;
    const toolName = pageTitle.split('|')[0].trim();
    
    // Detect Category based on Folder
    let categoryVerb = "Utility"; // Default
    if (currentUrl.includes('/generators/')) categoryVerb = "Generator";
    if (currentUrl.includes('/technical/')) categoryVerb = "Developer Tool";
    if (currentUrl.includes('/growth/')) categoryVerb = "Growth Engine";
    if (currentUrl.includes('/time-date/')) categoryVerb = "Time Engine";
    if (currentUrl.includes('/image-visual/')) categoryVerb = "Image Engine";

    // 1. Dynamic Meta Description
    if (!document.querySelector('meta[name="description"]')) {
        const meta = document.createElement('meta');
        meta.name = "description";
        // This creates: "Use the JSON Formatter on Rebrixe. A premium, private Developer Tool..."
        meta.content = `Use the ${toolName} on Rebrixe. A premium, 100% private ${categoryVerb} built for speed and data sovereignty. No data leaves your browser.`;
        document.head.appendChild(meta);
    }

    // 2. Canonical Tag (Crucial for avoiding "Dead Weight" duplicate content)
    if (!document.querySelector('link[rel="canonical"]')) {
        const canonical = document.createElement('link');
        canonical.rel = "canonical";
        canonical.href = currentUrl.split('?')[0].split('#')[0]; // Cleans URLs
        document.head.appendChild(canonical);
    }

    // 3. Social Media Tags (Open Graph)
    const ogData = {
        'og:title': `${toolName} | Rebrixe`,
        'og:description': `Fast, private ${categoryVerb} for modern creators.`,
        'og:url': currentUrl
    };

    Object.entries(ogData).forEach(([prop, content]) => {
        if (!document.querySelector(`meta[property="${prop}"]`)) {
            const m = document.createElement('meta');
            m.setAttribute('property', prop);
            m.content = content;
            document.head.appendChild(m);
        }
    });
}
document.addEventListener("DOMContentLoaded", initRebrixe);

function injectMeta() {
    const meta = `
        <meta property="og:title" content="Rebrixe | 500+ Premium Web Utilities">
        <meta property="og:description" content="A lightning-fast ecosystem for modern builders.">
        <meta property="og:image" content="https://Rebrixe.com/logo.png">
        <meta property="og:url" content="https://Rebrixe.com/">
        <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    `;
    document.head.insertAdjacentHTML('beforeend', meta);
}
injectMeta();

// Add this to the top or bottom of your nav.js
function injectMobileMeta() {
    // 1. The Black Address Bar (Mobile Chrome/Safari/Samsung)
    const themeMeta = document.createElement('meta');
    themeMeta.name = "theme-color";
    themeMeta.content = "#05070a"; // Matches your --bg variable
    document.head.appendChild(themeMeta);

    // 2. The Apple Status Bar (Specific for iPhones)
    const appleMeta = document.createElement('meta');
    appleMeta.name = "apple-mobile-web-app-status-bar-style";
    appleMeta.content = "black-translucent";
    document.head.appendChild(appleMeta);
}

// Run the function
injectMobileMeta();

function RebrixeSystemInit() {
    const siteUrl = "https://Rebrixe.com";
    
    // 1. Define the tags we need
    const tags = [
        { rel: 'icon', href: `${siteUrl}/favicon.png`, sizes: '48x48' },
        { rel: 'apple-touch-icon', href: `${siteUrl}/favicon.png` },
        { name: 'theme-color', content: '#05070a' }
    ];

    tags.forEach(tag => {
        // Check if the tag already exists to prevent collisions
        let element = tag.rel 
            ? document.querySelector(`link[rel="${tag.rel}"]`)
            : document.querySelector(`meta[name="${tag.name}"]`);

        if (!element) {
            // If it doesn't exist, create it
            element = document.createElement(tag.rel ? 'link' : 'meta');
            document.head.appendChild(element);
        }

        // Apply/Override the attributes to ensure Rebrixe branding is forced
        if (tag.rel) element.rel = tag.rel;
        if (tag.name) element.name = tag.name;
        if (tag.href) element.href = tag.href;
        if (tag.sizes) element.sizes = tag.sizes;
        if (tag.content) element.content = tag.content;
    });

    console.log("Rebrixe System: Branding & SEO injected successfully.");
}

// Initialize on load
RebrixeSystemInit();