module Main exposing (..)

import Commands exposing (fetchEntries)
import Html exposing (program)
import Keyboard
import Msgs exposing (Msg(..))
import Models exposing (Model, initialModel)
import Update exposing (update)
import View exposing (view)


init : (Model, Cmd Msg)
init =
    (initialModel, fetchEntries)

-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Keyboard.downs KeyMsg ]

-- MAIN


main : Program Never Model Msg
main =
    program
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }
