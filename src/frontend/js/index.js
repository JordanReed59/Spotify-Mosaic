const url = "https://af49q1sh2m.execute-api.***.amazonaws.com/test/mosaify";
const queryStringParameter = "test";
const queryStringParameterValue = 1234;

const data = {
    message:"Hello backend"
}

const otherParams = {
    headers:{
        "Content-Type" : "application/json; charset=UTF-8"
    },
    method:"POST",
    body:JSON.stringify(data),
    mode: 'no-cors'
}

fetch(url, otherParams)
    .then(res => {
        if (res.ok) {
            console.log(res)
        }
        else {
            console.log("response wasn't successful")
        }
    })
    // .then(data => data.json())
    .catch(error => console.log(error))