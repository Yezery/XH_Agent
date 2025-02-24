export class AppError extends Error {
  private error_messages: string[] | null

  constructor(message: string | null, error_messages: string[] | null = null) {
    super(message || 'Unknown error')
    this.name = 'AppError'
    this.error_messages = error_messages
  }

  getMessage(): string {
    if (this.error_messages && this.error_messages.length > 0) {
      return this.error_messages.join('.\n')
    }
    return this.message
  }

  getErrorMessages(): string[] {
    if (this.error_messages && this.error_messages.length > 0) {
      return this.error_messages
    }
    return [this.getMessage()]
  }
}

export function createAppError(e: unknown): AppError {
  if (e instanceof AppError) {
    return e
  }
  if (e && typeof e === 'object' && 'message' in e && typeof e.message === 'string') {
    return new AppError('Unexpected error: ' + e.message, null)
  }
  if (e && typeof e === 'object' && 'details' in e && typeof e.details === 'string') {
    return new AppError('Unexpected error: ' + e.details, null)
  }
  return new AppError('Unknown error', null)
}
