module View exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, href, property)
import Json.Encode
import Models exposing (Model, Entry, Fetched)
import Msgs exposing (Msg)


view : Model -> Html Msg
view model =
    div []
        [ currentRow model.current
        , unreadEntries model.unread              
        , unreadCounter model.unreadCnt
        ]


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


unreadEntries : List Entry -> Html Msg
unreadEntries entries =
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
                

unreadCounter : Maybe Int -> Html Msg
unreadCounter maybeCnt =
    case maybeCnt of
        Just unreadCnt ->
            div [ class "unread-counter" ]
                [ text (toString(unreadCnt) ++ " unread") ]

        Nothing ->
            text "no count yet"

