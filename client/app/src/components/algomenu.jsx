import React, { useState } from 'react';
import { Checkbox, MenuList, MenuItem } from '@mui/material';
import { algoNamesRus } from '../config';

const AlgoMenu = ({ selectedAlgorithms, onMenuItemSelect }) => {
  const [selectedMenuItem, setSelectedMenuItem] = useState(null);

  const handleMenuItemClick = (index) => {
    setSelectedMenuItem(index);
    onMenuItemSelect(index);
  };

  return (
    <div style={{border: "1px solid", display: "flex"}}>
      <MenuList>
        {selectedAlgorithms && Object.keys(selectedAlgorithms).map((key, ind) => (
          <MenuItem
            key={key}
            sx={{
              fontSize: 20,
              backgroundColor: selectedMenuItem === ind ? '#2196f3' : 'transparent',
              color: selectedMenuItem === ind ? '#fff' : 'inherit',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <Checkbox></Checkbox>
              <div onClick={() => handleMenuItemClick(ind)}>
                {algoNamesRus[ind]} | {selectedAlgorithms[key].toString()}
              </div>
            </div>
          </MenuItem>
        ))}
      </MenuList>
    </div>
  );
};

export default AlgoMenu;

