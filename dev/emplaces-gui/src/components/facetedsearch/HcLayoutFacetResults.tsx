import React from 'react';
import HcFacetBasic from "./HcFacetBasic";
import HcFacetTextSearch from './HcFacetTextSearch';
import { HcResultListHeader, HcResultList, HcResultSelectedFacets, HcResultListLegend, HcResultListPaging } from './HcResults';

export class HcLayoutFacetResults extends React.Component<{ pageName: String, data: GraphQlData }> {

  render() {
    return (
      <div className="hcContentContainer">

        <div className="hcBasicSideMargin hcMarginTop4 hcMarginBottom1">
          <h1>{this.props.pageName}</h1>
        </div>

        <div className="hcLayoutFacet-Result hcBasicSideMargin hcMarginBottom15">

          <div className="hcLayoutFacets">
            <button type="button" name="button" id="showFacets" className="hcfixedSideButton">
              <img src="images/icons/icon-set-facets.svg" className="icon" alt="Click to open en close facets" />
            </button>

            <div className="hcLayoutFacetsToggel" id="hcLayoutFacetsToggel">
              <HcFacetTextSearch
                facetName="Text search"
              />
              <HcFacetBasic
                facetName="Dataset"
              />
              <HcFacetBasic
                facetName="Persons"
              />
            </div>
          </div>

          <div className="hcLayoutResults">
            <HcResultListHeader totalResults={this.getTotal()} />
            <HcResultSelectedFacets />
            <HcResultListLegend />
            <HcResultList />
            <HcResultListPaging />


          </div>


        </div>
      </div>
    );
  }

  getTotal(): string {
    if (this.props.data) {
      const dataSets = this.props.data.data.dataSets;

      if (dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"]) {
        const dataSet = dataSets["u38d24500551ccff8d2b0c4f84fc947f45934aa26__emplaces"];
        if (dataSet["em_PlaceList"]) {
          const collection = dataSet["em_PlaceList"];
          if (collection["total"]) {
            return "" + collection["total"];
          }
        }
      }
    }

    return "0";
  }
}

export class GraphQlData {
  "data": {
    "dataSets": any
  }
}