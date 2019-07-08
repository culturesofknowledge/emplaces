import React, {DOMElement} from 'react';

export default class HcEmPlaceItemHeader extends React.Component<{ title: string, isH1:boolean, hasProv:boolean }> {
  title: DOMElement<any, any>;
  constructor(props: { title: string, isH1:boolean, hasProv:boolean }) {
    super(props);
    this.title = props.isH1? React.createElement("h1", {}, props.title) : React.createElement("strong", {}, props.title)
  }

  render() {
    return (
      <div className="hcEmplacesItemHeader">
        <div className="hcEmplacesTitle">
          { this.title }
          <div className="hcTxtColorGreyMid hcSmallTxt">Info</div>
        </div>
        {/* if hasProv=={true}, the next line should be displayed*/}
        <div hidden={!this.props.hasProv} className="hcTxtColorGreyMid hcSmallTxt">Provenance</div>

      </div>
    );
  }
}