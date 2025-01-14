/** This file is part of natlib.
 * https://github.com/mvasilkov/natlib
 * @license MIT | Copyright (c) 2022, 2023 Mark Vasilkov
 */
'use strict'

import { FALSE, ShortBool, TRUE } from '../prelude.js'
import type { IVec2 } from '../Vec2'

/** Pointer controls class */
export class Pointer implements IVec2 {
    x: number
    y: number
    held: ShortBool

    readonly canvas: HTMLCanvasElement

    constructor(canvas: HTMLCanvasElement) {
        this.x = this.y = 0

        this.canvas = canvas
    }

    /** Set the pointer position relative to the canvas. */
    setPosition(event: MouseEvent | Touch) {
        const r = this.canvas.getBoundingClientRect()

        this.x = event.clientX - r.left
        this.y = event.clientY - r.top
    }

    /** Initialize the event handlers. */
    addEventListeners(target: GlobalEventHandlers) {
        // Mouse events
        target.addEventListener('mousedown', event => {
            event.preventDefault()

            this.held = TRUE
            this.setPosition(event)
        })

        target.addEventListener('mousemove', event => {
            event.preventDefault()

            this.setPosition(event)
        })

        target.addEventListener('mouseup', event => {
            event.preventDefault()

            this.held = FALSE
        })

        target.addEventListener('mouseleave', _event => {
            // Default action is none, so no event.preventDefault()

            this.held = FALSE
        })

        // Touch events
        target.addEventListener('touchstart', event => {
            event.preventDefault()

            this.held = TRUE
            this.setPosition(event.targetTouches[0]!)
        })

        target.addEventListener('touchmove', event => {
            event.preventDefault()

            this.setPosition(event.targetTouches[0]!)
        })

        target.addEventListener('touchend', event => {
            event.preventDefault()

            this.held = FALSE
        })

        target.addEventListener('touchcancel', _event => {
            // Default action is none, so no event.preventDefault()

            this.held = FALSE
        })
    }
}
