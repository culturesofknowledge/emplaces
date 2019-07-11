import React from "react";
import { Redirect } from "react-router";

export default class HcResultItemEmPlaces extends React.Component<ResultItem> {
  state = {
    redirect: false
  }
  
  constructor(props: ResultItem) {
    super(props);
    this.setRedirect = this.setRedirect.bind(this);
    this.renderRedirect = this.renderRedirect.bind(this);
  }
  

  setRedirect() {
    this.setState({redirect:true});
  }

  renderRedirect() {
    if(this.state.redirect) {
      return <Redirect to={this.props.id}/>
    }
  }

  render() {
    return (
      <React.Fragment>
        {this.renderRedirect()}
        <div className="hcListBasicResult" onClick={this.setRedirect}>
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
  "id": string;
}