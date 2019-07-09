import React from 'react';

export default class HcEmPlaceItemHeader extends React.Component<{ title: string, isH1:boolean, hasProv:boolean }> {
 
  render() {
    return (
      <div className="hcEmplacesItemHeader">
        <div className="hcEmplacesTitle">
          { this.props.isH1? React.createElement("h1", {}, this.props.title) : React.createElement("strong", {}, this.props.title) }
          <div className="hcTxtColorGreyMid hcSmallTxt">Info</div>
        </div>
        {/* if hasProv=={true}, the next line should be displayed*/}
        <div hidden={!this.props.hasProv} className="hcTxtColorGreyMid hcSmallTxt">Provenance</div>

      </div>
    );
  }
}