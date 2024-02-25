import { kebabCase } from 'lodash'

import Settings from './Settings'

export default { Settings }

const createPagesConf = ( pagesList ) =>
  pagesList.map( ( { name, roles } ) => ( {
    component: name,
    link: kebabCase( name ),
    roles,
    title: kebabCase( name ).split( '-' ).join( ' ' ),
  } ) )

const mainPages = [
  { name: 'Home' },
  { name: 'IngestData' },
  { name: 'EntityDatabase' },
  { name: 'ProductDatabase' },
  { name: 'RunReports' },
]

export const mainPagesConf = createPagesConf( mainPages )
