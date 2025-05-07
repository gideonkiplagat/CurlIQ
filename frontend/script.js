document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('imageUpload');
    const uploadBox = document.getElementById('uploadBox');
    const imagePreview = document.getElementById('imagePreview');
    const resultsSection = document.getElementById('resultsSection');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const faceShapeResult = document.getElementById('faceShapeResult');
    const hairstylesGrid = document.getElementById('hairstylesGrid');
    const salonsList = document.getElementById('salonsList');

    // Handle image upload preview
    imageUpload.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(event) {
                imagePreview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
                uploadBox.style.display = 'none';
                imagePreview.style.display = 'block';
                resultsSection.style.display = 'none';
                analyzeBtn.style.display = 'block';
            }
            
            reader.readAsDataURL(file);
        }
    });

    // Analyze button click handler
    analyzeBtn.addEventListener('click', async function() {
        const file = imageUpload.files[0];
        if (!file) {
            alert('Please upload an image first');
            return;
        }

        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing please wait...';

        try {
            const formData = new FormData();
            formData.append('image', file);

            // Send to backend
            const response = await fetch('http://192.168.1.102:5000/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Display results
            displayResults(data);
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred during analysis');
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze My Photo';
        }
    });

    function displayResults(data) {
        // Show results section
        resultsSection.style.display = 'block';
        
        // Display face shape
        faceShapeResult.textContent = data.face_shape || 'Could not determine';
        
        // Display hairstyles (mock data - replace with your actual data)
        const hairstyles = getHairstylesForShape(data.face_shape);
        hairstylesGrid.innerHTML = hairstyles.map(style => `
            <div class="hairstyle-card">
                <img src="assets/images/${style.image}" alt="${style.name}">
                <div class="hairstyle-info">
                    <h4>${style.name}</h4>
                    <p>${style.description}</p>
                </div>
            </div>
        `).join('');
        
        // Display salons
        if (data.recommended_salons && data.recommended_salons.length > 0) {
            salonsList.innerHTML = `
                <h3>Recommended Salons Near You</h3>
                <div class="salons-container">
                    ${data.recommended_salons.map(salon => `
                        <div class="salon-card">
                            <h4>${salon.name}</h4>
                            <p>Rating: ${salon.rating}/5</p>
                            <p>${salon.location}</p>
                            <button class="btn-book">Book Now</button>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }

    // Mock function - replace with your actual hairstyle data
    function getHairstylesForShape(shape) {
        const hairstyles = {
            oval: [
                { name: "Long Layers", image: "long-layers.jpg", description: "Great for oval faces" },
                { name: "Pixie Cut", image: "pixie.jpg", description: "Bold and stylish" }
            ],
            round: [
                { name: "Angular Bob", image: "angular-bob.jpg", description: "Creates definition" },
                { name: "Side Part", image: "side-part.jpg", description: "Lengthens face" }
            ],
            heart: [
                { name: "Angular Bob", image: "angular-bob.jpg", description: "Creates definition" },
                { name: "Side Part", image: "side-part.jpg", description: "Lengthens face" }
            ],
            // Add more shapes as needed
        };
        
        return hairstyles[shape.toLowerCase()] || [
            { name: "Classic Cut", image: "classic.jpg", description: "Works for most face shapes" }
        ];
    }
    function displayResults(data) {
        if (data.error) {
            resultsSection.innerHTML = `
                <div class="error-card">
                    <h3>Analysis Failed</h3>
                    <p>${data.error}</p>
                    <p>Please try with a different photo.</p>
                </div>
            `;
            return;
        }
        
        // ... rest of your display code
    }
});

