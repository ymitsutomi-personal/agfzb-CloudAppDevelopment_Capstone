/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');

var db;

function main(params) {

    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });

    db = cloudant.db.use('dealerships');
    
    var wkState = '';
    if (params.state) {
        wkState = params.state;
    }
    
    let docs = findByState(wkState);
    
    if (docs.body == "[]"){
        if (wkState == ''){
            docs.body = "The database is empty";
        } else {
            docs.body = "The state does not exist";
            console.log("AAA");
        }
    } else {
        docs.body = "The state does not exist";
    }
    
    return docs;
}



function findByState(wkState) {
    return new Promise((resolve, reject) => {
        db.find({
            'selector': {
                'st': {
                    '$regex': `.*${wkState}.*`
                }
            }
        }, (err, documents) => {
            if (err) {
                reject(err);
            } else {
                var wkBody;
                var wkStatus;
                if (documents.docs.length == 0){
                    wkStatus = 404;
                    if (wkState == ''){
                        wkBody = "The database is empty";
                    } else {
                        wkBody = "The state does not exist";
                    }
                } else {
                    wkArray = [];
                    for (let i = 0; i < documents.docs.length; i++) {
                        let wkElement = {
                            id: documents.docs[i].id,
                            short_name: documents.docs[i].short_name,
                            full_name: documents.docs[i].full_name,
                            city: documents.docs[i].city,
                            state: documents.docs[i].state,
                            st: documents.docs[i].st,
                            address: documents.docs[i].address,
                            zip: documents.docs[i].zip,
                            lat: documents.docs[i].lat,
                            long: documents.docs[i].long
                        }
                        wkArray.push(wkElement);
                    }
                    wkBody = wkArray;
                    wkStatus = 200;
                }
                
                resolve({ body: JSON.stringify(wkBody), statusCode: wkStatus });
            }
        });
    });
}
