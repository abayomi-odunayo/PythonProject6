/* =========================
   GLOBAL STYLES
========================= */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Roboto', sans-serif;
}

body {
    background: #f4f7fc;
    color: #1e1e1e;
}

/* =========================
   NAVBAR
========================= */

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 50px;
    background: #0066ff;
    color: white;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.logo {
    font-size: 22px;
    font-weight: bold;
}

.nav-links {

    list-style: none;
    display: flex;
    gap: 20px;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-weight: 500;
}

.nav-links a:hover {
    text-decoration: underline;
}

/* =========================
   HERO SECTION
========================= */

.hero {
    height: 90vh;
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                url('https://images.unsplash.com/photo-1581091870622-1e7b2b1f3a7a') center/cover;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: white;
    padding: 20px;
}

.hero-content h1 {
    font-size: 45px;
    margin-bottom: 15px;
}

.hero-content p {
    font-size: 18px;
    margin-bottom: 20px;
}

.btn {
    padding: 12px 25px;
    background: #0066ff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    transition: 0.3s;
}

.btn:hover {
    background: #004bb5;
}

/* =========================
   SERVICES
========================= */

.services {
    padding: 60px 20px;
    text-align: center;
}

.service-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

/* =========================
   ABOUT SECTION
========================= */

.about-preview {
    padding: 60px 20px;
    background: #ffffff;
    text-align: center;
}

/* =========================
   FOOTER
========================= */

footer {
    background: #1e1e1e;
    color: white;
    text-align: center;
    padding: 20px;
    margin-top: 40px;
}

footer .socials a {
    color: #ccc;
    margin: 0 10px;
    text-decoration: none;
}

footer .socials a:hover {
    color: white;
}

/* =========================
   RESPONSIVE DESIGN
========================= */

@media (max-width: 768px) {

    .navbar {
        flex-direction: column;
        text-align: center;
    }

    .nav-links {
        flex-direction: column;
        margin-top: 10px;
    }

    .hero-content h1 {
        font-size: 30px;
    }
}