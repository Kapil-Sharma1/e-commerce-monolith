import React, { useContext, useEffect } from 'react'
import { Outlet, useNavigate } from 'react-router'
import { isEmpty } from 'lodash'

import AuthContext from '../../common/auth/auth'

const PrivateRoute = () => {
  const navigate = useNavigate()

  const { isLoggedIn, userData, fetchUserData } = useContext( AuthContext )

  useEffect( () => {
    if ( !userData ) {
      fetchUserData()
    }
  }, [ userData, fetchUserData ] )

  useEffect( () => {
    if ( !isLoggedIn() ) {
      navigate( '/login' )
    }
  } )

  if ( isEmpty( userData?.info ) ) {
    return null
  }

  return <Outlet />
}

export default PrivateRoute
