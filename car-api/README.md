Routes specification for the car-api (subject to change)

This is all the GET methods. You use them, when you want to get some information from the backend!

GET "/brands"
Returns a JSON object, containing two lists. The first one is the brand IDs, the second one is the name of the actual brand.

Volatility: May be removed in favor of a new search system.

Tip:
Lets say you want to find what is the name of a brand, from its ID. Call this route, and search the list that contains the IDs.
When you find the index of the ID you are looking for, use that same index in the other list, and you will get back the name of the brand,  

GET "/models/`<brand_id>`"<br>
Returns a JSON object, containing two lists. The first one is the model IDs, the second one is the name of the actual model.

Volatility: May be removed in favor of a new search system.

Tip:
Lets say you want to get a list of all models for a brand, so you can create a dropdown menu, based on the brand selected.
Call this, and access the second list!

GET "/carlist/`<brand_id>`"<br>
Returns a list of JSON objects, that represent all ADs, for a giving car brand. Each object, contains the AD id (hint: use for link generation on the list page), how many killomenters has the car done, its model ID, and its year. 

Volatility: May be change based on how the new search system evolves.

GET "/brandfromad/`<id>`"<br>
Returns a JSON object, that contains the brand ID for a given AD. 

Volatility: I don't know.

Tip:
You can use this, in combination with /brands, to find the brand name of a AD, just from that AD id.

GET "/car/`<id>`"<br>
Returns a JSON object, that contains the details for a specific AD.

Volatility: Won't change, but may give different info/have different fields.

Tip:
Use this for the car page.

This is all the POST methods. You use them, when you want to get some information from the backend!<br>

POST "/car"<br>
Call this when you want to add a car ad to the system. IMPORTANT! Make sure that when you call this, you make a POST request. By default, requests will make a GET request.
In order for it to work, you need to submit the request, with a valid JSON body. An example body, would look like this:

{
    "model": `<model id>`,<br>
    "year": `<year>`,<br>
    "km": `<km that the car has done>`,<br>
    "cardescr": `<car description>`,<br>
    "imgsrc": [`<link to img1>`, `<link to img2>`, `<... and so on>`]<br>
}<br>

Volatility: The JSON body's format, will most likely change, but the route itself probably won't.

Tip:
Use this to make the page for making an AD.

POST "/edit/`<id>`"<br>
Call this when you want to edit a car ad. IMPORTANT! Make sure that when you call this, you make a POST request. By default, requests will make a GET request.
In order for it to work, you need to submit the request, with a valid JSON body. An example body, would look like this:

{
    "year": `<updated year>`,
    "km": `<updated km that the car has done>`,
    "cardescr": `<new car description>`
}

Volatility: The JSON body's format, will change, but the route itself probably won't.

Tip:
Use this to make the page for making an AD.