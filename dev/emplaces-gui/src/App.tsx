import React from 'react';
import HcHeaderTimbuctoo from './components/HcHeaderTimbuctoo';
import './css/huc-connect-sets.css'
import './css/huc-data-entry.css'
import './css/huc-search.css'
import './css/remote.scss'

const App: React.FC = () => {
  return (
      <HcHeaderTimbuctoo></HcHeaderTimbuctoo>
  );
}

export default App;
  
document.title = "EMPlaces";
