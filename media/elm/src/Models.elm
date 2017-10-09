module Models exposing (..)


-- the data as returned from the backend
type alias Fetched =
    { unread : Int
    , entries : List Entry
    }

-- more useful structure for it.
type alias Model =
    { read : List Entry
    , current : Maybe Entry
    , unread : List Entry
    , unreadCnt : Maybe Int
    }

initialModel : Model
initialModel =
    { read = []
    , current = Nothing
    , unread = []
    , unreadCnt = Nothing
    }

-- the individual entries    
type alias EntryId = Int

type alias Entry =
    { id : EntryId
    , title : String
    , link : String
    , description : String
    , published : String
    , feed_title : String
    }

-- the simple data that is returned when we mark an entry as read
type alias EntryUpdate =
    { unread : Int }
