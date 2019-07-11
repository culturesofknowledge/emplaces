export function instanceOfEMPlace(object: any): object is EMPlace {
  
  return object.hasOwnProperty("uri") && object["uri"] != null
  && object["title"] != null && object["title"]["value"] != null 
  && ("em_placeType" in object) 
  && ("em_alternateNameList" in object) && ("items" in object["em_alternateNameList"]) && object["em_alternateNameList"]["items"] !== null;
}

export class EMPlace {
  "uri": string;
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

export class Value {
  "value": string;
}


export class SinglePlace {
  alternateNameList: string[];
  title: string;
  currentHierarchy: string[];
  alternateAuths: Link[];

  constructor(title: string, alternateNameList: string[], hierarchies: QualifiedRelation[], alternateAuths: Link[]) {
    this.title = title;
    this.alternateNameList = alternateNameList;
    this.currentHierarchy = getFirstCurrentHierarchy(title, hierarchies);
    this.alternateAuths = alternateAuths;
  }
}

function getFirstCurrentHierarchy(title:string , hierarchies: QualifiedRelation[]): string[] {
  return hierarchies.filter(hierarchy => instanceOfQualifiedRelation(hierarchy)).map(hierarchy => createCurrentHierarchy(title, hierarchy))[0];
}

function createCurrentHierarchy(currentName: string, hierarchy: QualifiedRelation): string[] {
  const hierarchyArray: QualifiedRelation[] = [];

  createHierarchyArray(hierarchy, hierarchyArray);

  const currentHierarchy = [currentName]; 
  
  hierarchyArray.filter(rel => rel.em_relationTo.hasOwnProperty("title"))
                .map(rel => {
                  if(rel.em_relationTo.em_preferredName) {
                    return rel.em_relationTo.em_preferredName.value;
                  }
                  return rel.em_relationTo.title.value;
                } )
                .forEach(place => currentHierarchy.push(place));

  return currentHierarchy;
}

function createHierarchyArray(start: QualifiedRelation, coll: QualifiedRelation[]) {
  coll.push(start);
  if (start.em_relationTo.em_hasRelation) {
    createHierarchyArray(start.em_relationTo.em_hasRelation, coll);
  }
}

function instanceOfQualifiedRelation(object: any) : object is QualifiedRelation {
  return object["em_relationType"] && object["em_relationType"]["title"]
  && object.hasOwnProperty("em_when") && instanceOfWhen(object["em_when"])
  && object.hasOwnProperty("em_relationTo"); 
}

function instanceOfWhen(object: any) : object is When {
 return object.hasOwnProperty("rdfs_label") 
 && object.hasOwnProperty("em_timespanList") && object["em_timespanList"]["items"].every((timeSpan:any) => instanceOfTimespan(timeSpan));
}

function instanceOfTimespan(object: any): object is TimeSpan {
  return object.hasOwnProperty("em_latestStart_") && object.hasOwnProperty("em_earliestEnd_");
}

export class Link {
  label: string;
  uri: string;
  constructor(label: string, uri: string) {
    this.label = label;
    this.uri = uri;
  }
}

export class QualifiedRelation {
  "em_relationType": {
    "title": Value
  }
  "em_timespan": {
    "em_when": When
  }
  "em_relationTo": RelatedPlace
}

class TimeSpan {
  "em_latestStart_": Value | null;
  "em_earliestEnd_": Value | null;
}

class When {
  "rdfs_label": Value | null
  "em_latestStart_": Value | null
  "em_earliestEnd_": Value | null
}

class RelatedPlace {
  "title": {
    "value": string
  }
  "em_preferredName": Value | null
  "em_placeCategory": {
    "rdfs_label": Value | null
  }
  "em_hasRelation": QualifiedRelation
}
