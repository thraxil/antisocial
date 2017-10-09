module Entries.List exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, href, property)
import Json.Encode
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


currentRow : Maybe Entry -> Html Msg
currentRow maybeEntry =
    case maybeEntry of
        Just entry ->
            div [ class "current expanded" ]
                [ div [ class "row" ]
                      [ div [ class "span11 title lead"]
                            [ a [ href entry.link ] [ text entry.title ]
                            , span [ class "published pull-right" ] [ text entry.published ]
                            ]
                      ]
                , div [ class "row" ]
                    [ div [ class "span10 feed-title"]
                          [ text "from "
                          , text entry.feed_title
                          ]
                    ]
                , div [ class "row" ]
                    [ div [class "span10 body"]
                          [ span [ property "innerHTML" (Json.Encode.string entry.description)]
                                []
                          ]
                    ]
                ]

        Nothing ->
            text ""
            

entryRow : Entry -> Html Msg
entryRow entry =
    div [ class "row" ]
        [ div [ class "span11 not-current title" ]
              [ text (entry.feed_title ++ ": " ++ entry.title)
              , span [ class "published pull-right" ] [ text entry.published ]
              ]
        ]
