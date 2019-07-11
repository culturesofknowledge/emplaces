import React from 'react';

export default class HcHeaderTimbuctoo extends React.Component {
  render() {
    return (
      <React.Fragment>
        <div className="hcContentContainer bgColorBrand1 hcMarginBottom5">
          <header className="hcPageHeaderSimple hcBasicSideMargin">
            {/* eslint-disable-next-line */}
            <a href="/" className="hcBrand">
              <div className="hcBrandLogo">
                <img src="https://d33wubrfki0l68.cloudfront.net/f268c733451856e103a2959ba15ffdaec6334ea4/d34d8/images/emlo-logo.png" className="logo" alt="EM Places" />
              </div>
            </a>

            <nav>
              {/* eslint-disable-next-line */}
              <a href="#">All datasets</a>
              {/* eslint-disable-next-line */}
              <a href="#">About</a>
            </nav>
          </header>
        </div>
        {/* <div className="hcContentContainer hcMarginBottom5 hcBorderBottom">
          <div className="hcBarDataset hcBasicSideMargin">
            <span>
              <span className="hcSmallTxt hcTxtColorGreyMid">Dataset</span>
              <select  >
                <option >**List all datasets**</option>
              </select>

            </span>
            <span>
              <span className="hcSmallTxt hcTxtColorGreyMid"> Collections</span>
              <select  >
                <option >**List all Properties of selected datasets**</option>
              </select>
            </span>
          </div>
        </div> */}
      </React.Fragment>
    );
  }
}