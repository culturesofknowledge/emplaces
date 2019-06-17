import React from 'react';

export default class HcFooterTimbuctoo extends React.Component {

  render() {
    return (
      <div className="hcContentContainer bgColorBrand1">
        <div className="hcMarginTop5 hcMarginBottom5 hc2columns">
          <div className="hcBasicSideMargin">
            <strong>Powered by Timbuctoo.</strong><br />
            Timbuctoo lets you fully exploit your Arts and Humanities data.
        It features powerful tools for data management and analysis, and allows you to connect your data with other datasets. <a href="https://timbuctoo.huygens.knaw.nl/">Learn more about Timbuctoo.</a>

          </div>
          <div className="hcBasicSideMargin">
            <img
              src="https://d33wubrfki0l68.cloudfront.net/e9bf56438b50ed9f97250de6d7c33b3bb8879741/c0f8e/images/logo-tim-hi-huc.png"
              alt="Timbuctoo Logo's"
              className="hcMarginTop2" />
          </div>
        </div>
      </div>
    );
  }
}