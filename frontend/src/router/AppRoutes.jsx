import React from 'react'
import { useRoutes, Navigate } from 'react-router-dom'

import AppLayout from '../../layouts/AppLayout'
import AuthLayout from '../../layouts/AuthLayout/AuthLayout'
import pages, { mainPagesConf, userPagesConf } from '../../pages'
import Auth from '../../pages/Auth'

const AppRoutes = () => {

  const createRouteProps = ( pagesConf ) =>
    pagesConf
      .map( ( { component, link } ) => {
        const Element = pages[component]

        return {
          element: <Element />,
          path: `${ link }/*`,
        }
      } )

  const appPages = createRouteProps( mainPagesConf )
  const userPages = createRouteProps( userPagesConf )

  const element = useRoutes( [
    {
      children: [
        {
          element: <Navigate to='/home' />,
          path: '',
        },
        ...appPages,
        ...userPages,
        {
          element: <Navigate to='/home' />,
          path: '*',
        },
      ],
      element: <AppLayout />,
    },
    {
      children: [
        {
          element: <Auth defaultPage='Login' />,
          path: '/login',
        },
        {
          element: <Auth defaultPage='ForgotPassword' />,
          path: '/forgot-password',
        },
        {
          element: <Auth defaultPage='ChangePassword' />,
          path: '/change-password/:uid/:token',
        },
      ],
      element: <AuthLayout />,
    },
  ] )

  return element
}

export default AppRoutes
