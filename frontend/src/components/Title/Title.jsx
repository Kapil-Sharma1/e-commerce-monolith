import React from 'react'
import { Helmet } from 'react-helmet-async'
import { useLocation } from 'react-router'
import { startCase } from 'lodash'

const Title = () => {
  const location = useLocation()

  const currentTitle = location.pathname
    .slice( 1 )
    .split( '/' )
    .shift()

  return (
    <Helmet>
      <title>
        Project Name - {currentTitle ? `- ${ startCase( currentTitle ) }` : ''}
      </title>
    </Helmet>
  )
}

export default Title
