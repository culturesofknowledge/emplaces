import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import HcFooterTimbuctoo from './components/HcFooterTimbuctoo'
import { HcLayoutFacetResults, GraphQlData } from './components/facetedsearch/HcLayoutFacetResults';
import fetch from 'node-fetch'

export default class FacetedSearch extends React.Component {
  state: {
    data: GraphQlData
  }
  query: string;

  constructor(props: {data?: GraphQlData}) {
    super(props);
    this.state = {
      data: {
        data: {
          dataSets: {}  
        }
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
        this.setState({ data: json });
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
    return object["data"] && object["data"]["datasets"];
  }
}
