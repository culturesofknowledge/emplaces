export class GraphQlData {
  "data": {
    "dataSets": any;
  };
}

export function instanceOfGraphQlData(object: any): object is GraphQlData {
  return object["data"] && object["data"]["dataSets"];
}

export class GraphQLCollection {
  "prevCursor": string | null
  "nextCursor": string | null
  "total": number
  "facets": []
  "items": any[]
}
