import { writable } from 'svelte/store';

export const currentResult = writable(null);
export const plantCollection = writable([]);
export const isLoading = writable(false);
export const collectionLoading = writable(false);
export const activeTab = writable('identify');
