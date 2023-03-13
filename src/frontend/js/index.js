const url = "https://af49q1sh2m.execute-api.us-east-1.amazonaws.com/test/mosaify";
const queryStringParameter = "test";
const queryStringParameterValue = 1234;

const data = {
    message:"Hello backend"
};

const otherParams = {
    headers:{
        "Content-Type" : "application/json; charset=UTF-8"

    },
    method:"POST",
    body:data,
    mode: 'no-cors'
};

fetch(url, otherParams)
// .then(data=>{return data.json()})
// .then(res=>{console.log(res)})
// .catch(error=>console.log(error));