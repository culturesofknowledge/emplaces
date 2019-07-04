import React from "react";

export default class HcResultItemEmPlaces extends React.Component<ResultItem> {
  render() {
    return (
      <React.Fragment>
        <div className="hcListBasicResult">
          <div className="hcListItemLong"><strong>{this.props.resultItemName}</strong><br />{this.props.resultItemAdministration}</div>
          <div>{this.props.resultItemType}</div>
          <div style={{
            display: 'flex',
            flexDirection: 'column',
          }}>
            {/* { this.props.resultItemAltNames} */}

            {this.props.resultItemAltNames.map(altName => (
              <span key={Math.random()}>{altName}</span>
            ))}

          </div>
        </div>

      </React.Fragment>
    );
  }
}

class ResultItem { 
  "resultItemName": string;
  "resultItemAdministration": string;
  "resultItemType": string;
  "resultItemAltNames": string[];
}