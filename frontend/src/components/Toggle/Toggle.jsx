import React from 'react'

import './Toggle.scss'

const Toggle = ( { label, ...rest } ) => (
  <div className='toggle-container'>
    <span>{label}</span>
    <input class='toggle' id='cb1' type='checkbox' { ...rest } />
    <label class='toggle-btn' for='cb1' />
  </div>
)

export default Toggle
