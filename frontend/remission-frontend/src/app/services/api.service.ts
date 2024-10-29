import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

// Injectable decorator to allow the service to be used in any component
@Injectable({
  providedIn: 'root'  // Provided in root scope to make it globally available
})
export class ApiService {
  // Backend API base URL
  private baseUrl = 'http://localhost:5000/api';  // Update this if your backend URL changes

  constructor(private http: HttpClient) {}

  /**
   * Log symptoms for a user.
   * @param symptomData Object containing symptom data (pain level, stress, etc.)
   * @returns Observable for API response
   */
  logSymptoms(symptomData: any): Observable<any> {
    const url = `${this.baseUrl}/log-symptoms`;
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post(url, symptomData, { headers });
  }

  /**
   * Get all logged symptoms for the current user.
   * @returns Observable for logged symptom data
   */
  getSymptomLogs(): Observable<any> {
    const url = `${this.baseUrl}/symptom-logs`;
    return this.http.get(url);
  }

  /**
   * Get trend analysis from CHIIP, the bot.
   * @returns Observable for bot analysis response
   */
  getBotAnalysis(): Observable<any> {
    const url = `${this.baseUrl}/bot-analysis`;  // Assuming the backend provides this endpoint
    return this.http.get(url);
  }
}
