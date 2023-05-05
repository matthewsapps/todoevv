export type TextBlock = {
    element: string
    text: string
    href?: string
    src?: string
}

export type Todo = {
    title: string
    tags: string[]
    description: TextBlock[]
    daysOfWeek: number[]
}