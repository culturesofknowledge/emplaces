import React from "react";

export default class HcEmPlaceCalendar extends React.Component<{date: string, percent: string}> {
  render() {
    return (
      <React.Fragment>
        {/* The percentage (here 23%) needs to be dynamic fro the var percent */}
      <div className="hcEmplCalMarker" style={{ marginLeft: this.props.percent }}>
        <span>{this.props.date}</span> 
        <span className="hcTxtColorGreyMid hcSmallTxt">(Inferred)</span> 
        </div>
      <div className="hcEmplCalBarLegend">
        <div className="hcTxtColorGreyMid hcSmallTxt">1500</div>
        <div className="hcTxtColorGreyMid hcSmallTxt">1800</div>
      </div>

      <div className="hcEmplCalBar">
        <div className="hcEmplCalBarSpace bgColorBrand1  hcSmallTxt" style={{ width: this.props.percent }}>Julian (Jan. 1)</div>
        <div className="hcEmplCalBarSpace hcSmallTxt" style={{width: 'calc(100% - ' + this.props.percent + ')'}}>Gregorian</div>
      </div>
    </ React.Fragment>
    );
  }
}