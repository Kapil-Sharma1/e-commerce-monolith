import React, { useEffect, useRef, useState } from 'react'
import classNames from 'classnames'

import './Collapsible.scss'

import { ArrowDownIcon } from '../../assets/icons'

import Icon from '../Icon'

const Collapsible = ( {
  children,
  title,
  extraClassName,
  CustomTitle = null,
  forceOpen = false,
  defaultOpen = false,
} ) => {
  const [ showContent, setShowContent ] = useState( defaultOpen )

  const contentRef = useRef()

  useEffect( () => {
    if ( contentRef.current ) {
      if ( showContent ) {
        contentRef.current.style.maxHeight = `${ contentRef.current.scrollHeight }px`
      } else {
        contentRef.current.style.maxHeight = '0px'
      }
    }
  }, [ showContent ] )

  useEffect( () => {
    if ( forceOpen ) setShowContent( true )
  }, [ forceOpen ] )

  const toggle = () => {
    setShowContent( ( old ) => !old )
  }

  return (
    <div className={ `collapsible-container ${ extraClassName }` }>
      <div className='title-section' onClick={ toggle }>
        {!CustomTitle ? <h5>{title}</h5> : <CustomTitle />}

        <Icon
          IconComponent={ ArrowDownIcon }
          className={ classNames( {
            'dark md pointer': true,
            rotate: showContent,
          } ) }
        />
      </div>

      <div className='collapsible-content' ref={ contentRef }>
        {children}
      </div>
    </div>
  )
}

export default Collapsible
