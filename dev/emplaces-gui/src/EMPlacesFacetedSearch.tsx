import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo'
import { HcLayoutFacetResults } from './components/facetedsearch/HcLayoutFacetResults';
import fetch from 'node-fetch'
import { SearchResult, ResultItem, Property } from './components/facetedsearch/SearchResult';

export default class FacetedSearch extends React.Component {
  state: {
    data: SearchResult
  }
  query: string;

  constructor(props: { data?: GraphQlData }) {
    super(props);
    this.state = {
      data: {
        total: 0,
        results: []
      }
    };
    this.query = "query emplaces ($esQuery:String) {\n  dataSets {\n    u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces {\n      em_PlaceList(elasticsearch: $esQuery) {\n        total\n        items {\n          title {\n            value\n          }\n          em_placeType {\n            ... on u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces_skos_Concept {\n              title {\n                value\n              }\n            }\n          }\n          em_alternateNameList {\n            items {\n              ... on u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces_value_xsd_string {\n                value\n              }\n              ... on u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces_value_rdf_langString {\n                value\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}"
  }

  componentDidMount() {
    fetch("https://repository.huygens.knaw.nl/v5/graphql", {
      "method": "POST",
      "body": JSON.stringify({
        "query": this.query,
        "operationName": "emplaces",
        "variables": {
          "esQuery": "{}"
        }
      }),
      headers: { 'Content-Type': 'application/json' }
    }).then(resp => resp.json())
      .then(json => {
        if (this.instanceOfGraphQlData(json)) {
          this.setState({ data: new SearchResult(this.getTotal(json), this.getData(json)) });
        }
      });
  }

  render() {
    return (
      <div className="App">
        <HcHeaderTimbuctoo></HcHeaderTimbuctoo>
        <HcLayoutFacetResults pageName="Place search" data={this.state.data}></HcLayoutFacetResults>
        <HcFooterTimbuctoo></HcFooterTimbuctoo>
      </div>
    );
  }

  instanceOfGraphQlData(object: any): object is GraphQlData {
    return object["data"] && object["data"]["dataSets"];
  }

  getData(data: GraphQlData): ResultItem[] {
    const resultData: ResultItem[] = [];
    if (data.data.dataSets) {
      const dataSets = data.data.dataSets;

      if (dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"]) {
        const dataSet = dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"];
        if (dataSet["em_PlaceList"]) {
          const collection = dataSet["em_PlaceList"];
          if (collection["items"]) {
            for (let item of collection["items"]) {
              if (this.instanceOfEMPlace(item)) {
                const property1 = new Property("PLACE", item.title.value);
                const property2 = new Property("PLACE TYPE", item.em_placeType.title.value ? item.em_placeType.title.value : "");
                const property3 = new Property("ALTERNATIVE NAMES", item.em_alternateNameList.items.map(value => value.value ? value.value: ""));
                resultData.push(new ResultItem(property1, property2, property3));
              }
            }
          }
        }
      }

    }
    return resultData;
  }

  getTotal(data: GraphQlData): number {
    if (data.data.dataSets) {
      const dataSets = data.data.dataSets;
      if (dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"]) {
        const dataSet = dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"];
        if (dataSet["em_PlaceList"]) {
          const collection = dataSet["em_PlaceList"];
          if (collection["total"]) {
            return collection["total"];
          }
        }
      }
    }

    return 0;
  }

  instanceOfEMPlace(object: any): object is EMPlace {
    return object["title"] && object["title"]["value"]
      && object["em_placeType"] && object["em_placeType"]["title"] && object["em_placeType"]["title"]["value"]
      && object["em_alternateNameList"] && object["em_alternateNameList"]["items"]
      ;
  }
}

class EMPlace {
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



class GraphQlData {
  "data": {
    "dataSets": any;
  }
}

