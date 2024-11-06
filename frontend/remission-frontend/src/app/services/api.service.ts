import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';
  private headers = new HttpHeaders({ 'Content-Type': 'application/json' });

  constructor(private http: HttpClient) {}

  /**
   * Logs symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.)
   * @returns Observable for API response
   */
  logSymptoms(symptomData: any): Observable<any> {
    const url = `${this.baseUrl}/log-symptoms`;
    return this.http.post(url, symptomData, { headers: this.headers })
      .pipe(
        catchError(this.handleError('logging symptoms'))
      );
  }

  /**
   * Retrieves all logged symptoms for the current user.
   * @returns Observable for logged symptom data
   */
  getSymptomLogs(): Observable<any> {
    const url = `${this.baseUrl}/symptom-logs`;
    return this.http.get(url)
      .pipe(
        catchError(this.handleError('fetching symptom logs'))
      );
  }

  /**
   * Fetches trend analysis insights from CHIIP.
   * @returns Observable for bot analysis response
   */
  getBotAnalysis(): Observable<any> {
    const url = `${this.baseUrl}/bot-analysis`;
    return this.http.get(url)
      .pipe(
        catchError(this.handleError('fetching bot analysis'))
      );
  }

  /**
   * Sends a user message to CHIIP and retrieves a response.
   * @param userMessage The message from the user to the bot
   * @returns Observable with the bot's response
   */
  getBotResponse(userMessage: string): Observable<any> {
    const url = `${this.baseUrl}/bot-response`;
    return this.http.post(url, { message: userMessage }, { headers: this.headers })
      .pipe(
        catchError(this.handleError('sending bot message'))
      );
  }

  /**
   * Handles errors from API calls and logs them.
   * Provides a default error message for user notification.
   * @param operation Description of the failed operation
   * @returns Observable with error information
   */
  private handleError(operation = 'operation') {
    return (error: any): Observable<never> => {
      console.error(`Error during ${operation}:`, error);
      alert(`An error occurred while ${operation}. Please try again later.`);
      return throwError(() => new Error('Something went wrong with the network request.'));
    };
  }
}
