document.addEventListener('DOMContentLoaded', function () {
    // Initialize form input variables
    const carMake = document.getElementById('make');
    const carModel = document.getElementById('model');
    const carYear = document.getElementById('year');
    const carMileage = document.getElementById('mileage');
    const imageCount = document.getElementById('imageCount');
    const listingPrice = document.getElementById('listingPrice');
    const analysisResult = document.getElementById('analysisResult');
    const analysisContent = document.getElementById('analysisContent');

    // Function to construct the ChatGPT prompt
    function constructPrompt(kbbPrice) {
        return `Analyze the legitimacy of this car listing based on the following details: Make: ${carMake.value}, Model: ${carModel.value}, Year: ${carYear.value}, Mileage: ${carMileage.value}, Number of Images: ${imageCount.value}, Listing Price: ${listingPrice.value}, Kelley Blue Book Price: ${kbbPrice}. Provide a detailed explanation and a legitimacy score from 0 to 10.`;
    }

    function showLoadingSpinner() {
        document.getElementById('loadingSpinner').style.display = 'block';
    }

    // Function to hide the loading spinner
    function hideLoadingSpinner() {
        document.getElementById('loadingSpinner').style.display = 'none';
    }

    async function fetchKBBPrice(make, model, year) {
        try {
            const response = await fetch(`http://localhost:5000/get_price?make=${make}&model=${model}&year=${year}`);
            const data = await response.json();
            console.log(data);
            return data.price;
        } catch (error) {
            console.error("Error fetching KBB price:", error);
            return null;
        }
    }

    // Function to handle the analyze button click
    document.getElementById('analyzeButton').addEventListener('click', async function () {
        showLoadingSpinner();
        let kbbPrice = await fetchKBBPrice(carMake.value, carModel.value, carYear.value);
        let prompt = constructPrompt(kbbPrice);

        let response = await fetch('/chatGPT', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: [{ role: "system", content: "The following task requires an analysis of automotive listings. The user will input details about a car's make, model, year, mileage, number of images from the posting, and the current listing price as shown on a social media marketplace. Your job is to use this information to assess whether the listing seems reasonable, overpriced, or potentially a scam. Consider factors such as the car's used market value, which is found through kelley blue book using a python webscraper, and common indicators of scams. Provide a detailed explanation of your assessment, including any red flags or positive indicators you identify. Finally, assign a legitimacy score from 0 to 10, with decimals allowed, where 10 signifies a highly legitimate listing and 0 indicates a high probability of being a scam. Your analysis will help the user make an informed decision about the listing." }, { role: "user", content: prompt }] })
        });
        let aiData = await response.json();
        hideLoadingSpinner();
        displayAnalysisResult(aiData, kbbPrice);
    });

    document.getElementById('checkPriceButton').addEventListener('click', async function () {
        showLoadingSpinner();
        let kbbPrice = await fetchKBBPrice(carMake.value, carModel.value, carYear.value);

        if (kbbPrice !== null) {
            analysisContent.innerHTML = `Kelley Blue Book Price: ${kbbPrice}`;
        } else {
            analysisContent.innerHTML = `Price could not be fetched from Kelley Blue Book.`;
        }
        analysisResult.style.display = 'block';
        hideLoadingSpinner();
    });

    // Function to display the analysis result
    function displayAnalysisResult(aiData, kbbPrice) {
        analysisContent.innerHTML = `Kelley Blue Book Price: ${kbbPrice}<br>AI Analysis: ${aiData.choices[0].message.content}`;
        analysisResult.style.display = 'block';
    }
});