import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo'
import { HcLayoutFacetResults } from './components/facetedsearch/HcLayoutFacetResults';
import fetch from 'node-fetch'
import { SearchResult, ResultItem, Property } from './components/facetedsearch/SearchResult';
import { instanceOfFacetData, Facet, FacetData } from './components/facetedsearch/Facet';
import { instanceOfEMPlace } from './EMPlace';

export default class FacetedSearch extends React.Component {
  dataSetId = "ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places";
  state: {
    data: SearchResult
  }
  query: string;

  private readonly collectionName = "em_PlaceList";

  constructor(props: { data?: GraphQlData }) {
    super(props);
    this.state = {
      data: {
        total: 0,
        results: [],
        facets: []
      }
    };
    this.query = "query emplaces($esQuery: String) {\n  dataSets {\n    ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places {\n      em_PlaceList(elasticsearch: $esQuery) {\n        total\n        facets {\n          caption\n          options {\n            name\n            count\n          }\n        }\n        items {\n          title {\n            value\n          }\n          em_placeType {\n            ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places_skos_Concept {\n              title {\n                value\n              }\n            }\n          }\n          em_alternateNameList {\n            items {\n              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places_value_xsd_string {\n                value\n              }\n              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places_value_rdf_langString {\n                value\n              }\n            }\n          }\n          em_hasRelationList {\n            items {\n              em_relationType {\n                em_toType {\n                  title {\n                    value\n                  }\n                }\n              }\n              em_relationTo {\n                ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places_em_Place {\n                  em_hasRelationList {\n                    items {\n                      em_relationType {\n                        em_toType {\n                          title {\n                            value\n                          }\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}"
  }

  componentDidMount() {
   this.executeQuery();
  }

  executeQuery() {

    

    fetch("https://repository.huygens.knaw.nl/v5/graphql", {
      "method": "POST",
      "body": JSON.stringify({
        "query": this.query,
        "operationName": "emplaces",
        "variables": {
          "esQuery": "{\"aggs\":{\"Place type\":{\"filter\":{},\"aggs\":{\"name\":{\"terms\":{\"field\":\"em_placeType.title.value.raw\"}}}},\"Calendars\":{\"filter\":{},\"aggs\":{\"name\":{\"terms\":{\"field\":\"em_hasAnnotationList.items.oa_hasBody.title.value.raw\"}}}},\"Authority\":{\"filter\":{},\"aggs\":{\"name\":{\"terms\":{\"field\":\"em_alternateAuthorityList.items.title.value.raw\"}}}}}}"
        }
      }),
      headers: { 'Content-Type': 'application/json' }
    }).then(resp => resp.json())
      .then(json => {
        if (this.instanceOfGraphQlData(json)) {
          this.setState({ data: new SearchResult(this.getTotal(json), this.getData(json), this.getFacets(json)) });
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

  getFacets(data: GraphQlData): Facet[] {
    if (data.data.dataSets) {
      const dataSets = data.data.dataSets;

      if (dataSets[this.dataSetId]) {
        const dataSet = dataSets[this.dataSetId];

        if (dataSet[this.collectionName]) {
          const collection = dataSet[this.collectionName];
          if (collection["facets"] instanceof Array && collection["facets"].every((item: any) => instanceOfFacetData(item))) {
            return collection["facets"].map((facetData: FacetData) => new Facet(facetData, () => this.executeQuery()));
          }
        }
      }
    }
    return [];
  }

  getData(data: GraphQlData): ResultItem[] {
    const resultData: ResultItem[] = [];
    if (data.data.dataSets) {
      const dataSets = data.data.dataSets;

      if (dataSets[this.dataSetId]) {
        const dataSet = dataSets[this.dataSetId];
        if (dataSet[this.collectionName]) {
          const collection = dataSet[this.collectionName];
          if (collection["items"]) {
            for (let item of collection["items"]) {
              if (instanceOfEMPlace(item)) {
                const property1 = new Property("PLACE", item.title.value);
                const property2 = new Property("PLACE TYPE", item.em_placeType && item.em_placeType.title && item.em_placeType.title.value ? item.em_placeType.title.value : "");
                const property3 = new Property("ALTERNATIVE NAMES", item.em_alternateNameList.items.map(value => value.value ? value.value : ""));
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
      if (dataSets[this.dataSetId]) {
        const dataSet = dataSets[this.dataSetId];
        if (dataSet[this.collectionName]) {
          const collection = dataSet[this.collectionName];
          if (collection["total"]) {
            return collection["total"];
          }
        }
      }
    }

    return 0;
  }
}

class GraphQlData {
  "data": {
    "dataSets": any;
  }
}

