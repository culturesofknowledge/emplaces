import React, { MouseEventHandler } from "react"
import { Facet } from "./Facet";

export default class HcFacetBasic extends React.Component<{ facet: Facet }> {
  render() {
    return (
      <div className="hcFacet">
        <div className="hcFacetTitle">
          <span>{this.props.facet.caption}</span>
          <span className="hcIconHelp"><img src="https://d33wubrfki0l68.cloudfront.net/85886ca3e2d8c36ba06d7773a094512272453181/545f8/images/icons/icon-huc-help.svg" alt="Click for info" /></span>
        </div>

        <div className="hcFacetHelp">
          <strong>The Source dataset facet </strong><br />
          Please note that the content is organised by archive folder. This may affect your results. Learn more about the structure of the archive.
        </div>



        <div className="hcFacetItems">
          {this.props.facet.options.map(option => { return <HcFacetItem key={Math.random()} facetItemName={option.name} facetItemAmount={ option.count} onclick={() => this.props.facet.optionSelected(option.name)} /> })}
          {/* eslint-disable-next-line */}
          {/* <a href="#">More</a> */}
        </div>
      </div>
    );
  }
}

class HcFacetItem extends React.Component<{ facetItemName: string, facetItemAmount: number, onclick: MouseEventHandler }> {
  render() {
    return (
      <div className="hcFacetItem" onClick={this.props.onclick}>
        {this.props.facetItemName} <span className="hcFacetCount">{this.props.facetItemAmount}</span>
      </div>
    );
  }
}