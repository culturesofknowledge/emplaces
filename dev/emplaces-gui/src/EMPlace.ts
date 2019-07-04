export function instanceOfEMPlace(object: any): object is EMPlace {
  return object["title"] != null && object["title"]["value"] != null 
  && ("em_placeType" in object) 
  && ("em_alternateNameList" in object) && ("items" in object["em_alternateNameList"]) && object["em_alternateNameList"]["items"] !== null;
}

export default class EMPlace {
  "title": {
    "value": string;
  }
  "em_placeType": {
    "title": Value;
  }
  "em_alternateNameList": {
    "items": Value[];
  }
}

class Value {
  "value": string | null;
}