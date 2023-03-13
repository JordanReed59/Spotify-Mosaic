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
    body:data,
    mode: 'no-cors'
}

fetch("https://regres.in/api/users", otherParams)
    .then(res => console.log(res))
    // .then(data => data.json())
    .catch(error => console.log(error))