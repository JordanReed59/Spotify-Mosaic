const url = "https://af49q1sh2m.execute-api.us-east-1.amazonaws.com/test/mosaify";
const resource = "/mosaify"
const queryStringParameter = "test";
const queryStringParameterValue = 1234;

const data = {
    message:"Hello backend"
}

const otherParams = {
    // headers:{
    //     "Content-Type" : "application/json; charset=UTF-8"
    // },
    method:"GET",
    // body:JSON.stringify(data),
    mode: 'no-cors'
}

fetch(url, otherParams) 
    .then(res => {
        console.log(res)
        // if (res.ok) {
        //     console.log('success!', res);
        // }
    })
    .catch(error => console.warn('Something went wrong.', error))
// fetch(url, otherParams)
//     .then(res => {
//         if (res.ok) {
//             console.log(res)
//         }
//         else {
//             console.log("response wasn't successful")
//         }
//     })
//     .then(data => data.json())
    // .catch(error => console.log(error))