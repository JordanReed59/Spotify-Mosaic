const url = "https://af49q1sh2m.execute-api.us-east-1.amazonaws.com/test/mosaify";
const queryStringParameter = "test";
const queryStringParameterValue = 1234;

const data = {
    img_data : "dkslkdakldfkdlfd",
    track_data : "djksahfj"
}

const otherParams = {
    headers:{
        "content-type" : "application/json; charset=UTF-8"

    },
    body:data,
    method:"POST"
}

fetch(url, otherParams)
.then(data=>{return data.json()})
.then(res=>{console.log(res)})
.catch(error=>console.log(error))