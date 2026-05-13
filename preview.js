function updatePreview() {
    // Existing fields
    document.getElementById("preview_name").innerText = 
        document.getElementById("full_name").value || "Your Name";
    
    document.getElementById("preview_email").innerText = 
        document.getElementById("email").value || "example@mail.com";
    
    document.getElementById("preview_phone").innerText = 
        document.getElementById("phone").value || "1234567890";
    
    document.getElementById("preview_linkedin").innerText = 
        document.getElementById("linkedin").value || "linkedin.com/in/username";
    
    // NEW FIELDS ADD PANNU
    document.getElementById("preview_objective").innerText = 
        document.getElementById("objective").value || "Your objective...";
    
    document.getElementById("preview_education").innerText = 
        document.getElementById("education").value || "Institution, Degree, Year";
    
    document.getElementById("preview_technical_skills").innerText = 
        document.getElementById("technical_skills").value || "HTML, CSS, Python";
    
    document.getElementById("preview_soft_skills").innerText = 
        document.getElementById("soft_skills").value || "Communication, Leadership";
    
    document.getElementById("preview_experience").innerText = 
        document.getElementById("experience").value || "Work experience...";
    
    document.getElementById("preview_profile").innerText = 
        document.getElementById("profile").value || "Professional summary...";
    
    document.getElementById("preview_declaration").innerText = 
        document.getElementById("declaration").value || "Your declaration...";
}

function changeTemplate(){
    let value = document.getElementById("templateSelect").value;
    document.getElementById("preview").className = value;
}
