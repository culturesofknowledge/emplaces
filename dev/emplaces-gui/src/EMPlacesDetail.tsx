import React from 'react';
import { match } from 'react-router';
import HcLayoutEmplacesDetail from './components/details/HcLayoutEmplacesDetail';
import {SinglePlace, Link, Value} from './EMPlace';
import { instanceOfGraphQlData, GraphQlData } from './GraphQlData';

export default class EmPlacesDetail extends React.Component<{ match: match<{ uri: string }> }> {
  private readonly collection = "em_Place";
  private readonly dataSetId = "ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705";
  private readonly query = "query singlePlace($uri: String!) {\n  dataSets {\n    ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705 {\n      em_Place(uri: $uri) {\n        em_preferredName {\n          value\n        }\n        title {\n          value\n        }\n        em_alternateNameList {\n          items {\n            ... on Value {\n              value\n            }\n          }\n        }\n        em_hasRelation {\n          ...recursiveRelation\n        }\n        em_alternateAuthorityList {\n          items {\n            ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Authority {\n              title {\n                value\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment recursiveRelation on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Qualified_relation {\n  ...relationFields\n  em_relationTo {\n    ...relatedPlace\n    ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n      em_hasRelation {\n        ...relationFields\n        em_relationTo {\n          ...relatedPlace\n          ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n            em_hasRelation {\n              ...relationFields\n              em_relationTo {\n                ...relatedPlace\n                ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                  em_hasRelation {\n                    ...relationFields\n                    em_relationTo {\n                      ...relatedPlace\n                      ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                        em_hasRelation {\n                          ...relationFields\n                          em_relationTo {\n                            ...relatedPlace\n                            ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                              em_hasRelation {\n                                ...relationFields\n                                em_relationTo {\n                                  ...relatedPlace\n                                  ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                                    em_hasRelation {\n                                      ...relationFields\n                                      em_relationTo {\n                                        ...relatedPlace\n                                        ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                                          em_hasRelation {\n                                            ...relationFields\n                                            em_relationTo {\n                                              ...relatedPlace\n                                              ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                                                em_hasRelation {\n                                                  ...relationFields\n                                                  em_relationTo {\n                                                    ...relatedPlace\n                                                    ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                                                      em_hasRelation {\n                                                        ...relationFields\n                                                        em_relationTo {\n                                                          ...relatedPlace\n                                                          ... on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n                                                            em_hasRelation {\n                                                              ...relationFields\n                                                              em_relationTo {\n                                                                ...relatedPlace\n                                                              }\n                                                            }\n                                                          }\n                                                        }\n                                                      }\n                                                    }\n                                                  }\n                                                }\n                                              }\n                                            }\n                                          }\n                                        }\n                                      }\n                                    }\n                                  }\n                                }\n                              }\n                            }\n                          }\n                        }\n                      }\n                    }\n                  }\n                }\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment relationFields on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Qualified_relation {\n  em_relationType {\n    title {\n      value\n    }\n  }\n  em_when {\n    rdfs_label {\n      value\n    }\n    em_timespan {\n      em_latestStart_ {\n        value\n      }\n      em_earliestEnd_ {\n        value\n      }\n    }\n  }\n}\n\nfragment relatedPlace on ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190705_em_Place {\n  title {\n    value\n  }\n  em_preferredName {\n    value\n  }\n  em_placeCategory {\n    rdfs_label {\n      value\n    }\n  }\n}";
  uri: string;
  state: {
    data: SinglePlace
  };


  constructor(props: { match: match<{ uri: string }> }) {
    super(props);
    this.uri = decodeURIComponent(props.match.params.uri);
    this.state = { data: this.dummySinglePlace() };
  }

  componentDidMount() {
    fetch("https://repository.huygens.knaw.nl/v5/graphql", {
      "method": "POST",
      "body": JSON.stringify({
        "query": this.query,
        "operationName": "singlePlace",
        "variables": {
          "uri": this.uri
        }
      }),
      headers: { 'Content-Type': 'application/json' }
    }).then(resp => resp.json())
      .then(json => {
        if (instanceOfGraphQlData(json)) {
          this.setState({ data: this.createSinglePlace(json) });
        }
      });
  }

  createSinglePlace(data: GraphQlData): SinglePlace {
    const dataSets = data.data.dataSets;

    if (dataSets[this.dataSetId]) {
      const dataSet = dataSets[this.dataSetId];

      if (dataSet[this.collection]) {
        const collection = dataSet[this.collection];

        return new SinglePlace(this.getTitle(collection), this.getAlternateNames(collection), this.getCurrentHierarchy(collection), this.getAuthorities(collection));
      }
    }

    return this.dummySinglePlace();
  }

  getAuthorities(collection: any): Link[] {
    
    if(collection.hasOwnProperty("em_alternateAuthorityList")) {
      console.log("auths: ", collection["em_alternateAuthorityList"]["items"]);

      return collection["em_alternateAuthorityList"]["items"].map((auth: { "title": Value; }) => new Link(auth["title"]["value"], "#"));
    }

    return [];
  }

  getAlternateNames(collection: any): string[] {
    return collection["em_alternateNameList"] ? collection["em_alternateNameList"]["items"].map( (item: { [x: string]: any; }) => item["value"]) : [];
  }

  getTitle(collection: any): string {
    return collection["em_preferredName"] ? collection["em_preferredName"]["value"] : "";
  }

  getCurrentHierarchy(collection: any) {
    return collection["em_hasRelation"] ? collection["em_hasRelation"]: {};
  }

  dummySinglePlace(): SinglePlace {
    return {
      title: "{title}",
      alternateNameList: ["{alternateNames}"],
      currentHierarchy: [], 
      alternateAuths: []
    };
  }

  render() {
    return <HcLayoutEmplacesDetail data={this.state.data} />;
  }
}