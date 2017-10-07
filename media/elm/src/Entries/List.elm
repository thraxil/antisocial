module Entries.List exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, href)
import Msgs exposing (Msg)
import Models exposing (Entry)


view : List Entry -> Html Msg
view entries =
    div []
        [ list entries ]


list : List Entry -> Html Msg
list entries =
    div []
        ( List.map entryRow entries )

entryRow : Entry -> Html Msg
entryRow entry =
    case entry.current of
        True ->
            div [ class "current" ]
                [ a [ href entry.link ]
                      [
                       h2 [] [ text entry.title ]
                      ]
                , div [] [ text entry.description ]
                ]

        False ->
            div [ class "row" ]
                [ div [ class "span11 not-current title" ]
                      [ text (entry.feed_title ++ ": " ++ entry.title)
                      , span [ class "published pull-right" ] [ text entry.published ]
                      ]
                ]
