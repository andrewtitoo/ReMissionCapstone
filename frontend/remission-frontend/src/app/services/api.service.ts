import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root' // Ensures the service is available application-wide
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api'; // Base URL for your API
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  /**
   * Creates a new user and returns a generated User ID.
   * @returns Observable containing the new User ID.
   */
  createUser(): Observable<any> {
    const url = `${this.baseUrl}/create-user`;
    return this.http.post(url, {}, { headers: this.headers }).pipe(
      catchError(this.handleError('creating new user'))
    );
  }

  /**
   * Validates if a given User ID exists in the system.
   * @param userId The User ID to validate.
   * @returns Observable for API response.
   */
  validateUserId(userId: number): Observable<any> {
    const url = `${this.baseUrl}/validate-user/${userId}`;
    return this.http.get(url, { headers: this.headers }).pipe(
      catchError(this.handleError('validating user ID'))
    );
  }

  /**
   * Logs symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.)
   * @param userId The ID of the user logging symptoms
   * @returns Observable for API response.
   */
  logSymptoms(symptomData: any, userId: number): Observable<any> {
    const url = `${this.baseUrl}/log-symptoms`;
    const payload = { ...symptomData, user_id: userId };
    return this.http.post(url, payload, { headers: this.headers }).pipe(
      catchError(this.handleError('logging symptoms'))
    );
  }

  /**
   * Retrieves all logged symptoms for the specified user.
   * @param userId The ID of the user to retrieve logs for.
   * @returns Observable for logged symptom data.
   */
  getSymptomLogs(userId: number): Observable<any> {
    const url = `${this.baseUrl}/symptom-logs?user_id=${userId}`;
    return this.http.get(url, { headers: this.headers }).pipe(
      catchError(this.handleError('fetching symptom logs'))
    );
  }

  /**
   * Sends a user message to CHIIP and retrieves a response.
   * @param userMessage The message from the user to the bot.
   * @returns Observable with the bot's response.
   */
  getBotResponse(userMessage: string): Observable<any> {
    const url = `${this.baseUrl}/bot-response`;
    const payload = { message: userMessage };
    return this.http.post(url, payload, { headers: this.headers }).pipe(
      catchError(this.handleError('sending bot message'))
    );
  }

  /**
   * Fetches trend analysis insights from CHIIP.
   * @param userId The ID of the user to analyze logs for.
   * @returns Observable for bot analysis response.
   */
  getBotAnalysis(userId: number): Observable<any> {
    const url = `${this.baseUrl}/bot-analysis`;
    const payload = { user_id: userId };
    return this.http.post(url, payload, { headers: this.headers }).pipe(
      catchError(this.handleError('fetching bot analysis'))
    );
  }

  /**
   * Generic error handler for API requests.
   * @param operation Description of the failed operation.
   * @returns Observable that throws an error.
   */
  private handleError(operation: string) {
    return (error: any): Observable<never> => {
      console.error(`Error during ${operation}:`, error); // Log to console for debugging
      alert(`An error occurred while ${operation}. Please try again later.`);
      return throwError(() => new Error('Something went wrong with the network request.'));
    };
  }
}
