module Entries.List exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class)
import Msgs exposing (Msg)
import Models exposing (Entry)


view : List Entry -> Html Msg
view entries =
    div []
        ( List.map entryRow entries )


entryRow : Entry -> Html Msg
entryRow entry =
    div [ class "row" ]
        [ div [ class "span11 not-current title" ]
              [ text (entry.feed_title ++ ": " ++ entry.title)
              , span [ class "published pull-right" ] [ text entry.published ]
              ]
        ]
