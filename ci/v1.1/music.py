"""
Python  API for the music service.
"""

# Standard library modules

# Installed packages
import requests


class Music():
    """Python API for the music service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s2:30001/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """
    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def create(self, artist, song, OrigArtist=None):
        """Create an artist, song pair.

        Parameters
        ----------
        artist: string
            The artist performing song.
        song: string
            The name of the song.
        OrigArtist: string or None
            The name of the original performer of this song.

        Returns
        -------
        (number, string)
            The number is the HTTP status code returned by Music.
            The string is the UUID of this song in the music database.
        """
        payload = {'Artist': artist,
                   'SongTitle': song}
        if OrigArtist is not None:
            payload['OrigArtist'] = OrigArtist
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['music_id']

    def write_OrigArtist(self, m_id, OrigArtist):
        """Write the original artist performing a song.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        OrigArtist: string
            The original artist performing the song.

        Returns
        -------
        number
            The HTTP status code returned by the music service.
        """
        r = requests.put(
            self._url + 'write_OrigArtist/' + m_id,
            json={'OrigArtist': OrigArtist},
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def read(self, m_id):
        """Read an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        status, artist, title, OrigArtist

        status: number
            The HTTP status code returned by Music.
        artist: If status is 200, the artist performing the song.
          If status is not 200, None.
        title: If status is 200, the title of the song.
          If status is not 200, None.
        OrigArtist: If status is 200 and the song has an
          original artist field, the artist's name.
          If the status is not 200 or there is no original artist
          field, None.
        """
        r = requests.get(
            self._url + m_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None, None, None

        item = r.json()['Items'][0]
        OrigArtist = (item['OrigArtist'] if 'OrigArtist' in item
                      else None)
        return r.status_code, item['Artist'], item['SongTitle'], OrigArtist

    def read_OrigArtist(self, m_id):
        """Read the orginal artist of a song.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        status, OrigArtist

        status: number
            The HTTP status code returned by Music.
        OrigArtist:
          If status is 200, the original artist who
            performed the song.
          If status is not 200, None.
        """
        r = requests.get(
            self._url + 'read_OrigArtist/' + m_id,
            headers={'Authorization': self._auth}
            )
        if r.status_code != 200:
            return r.status_code, None
        item = r.json()
        return r.status_code, item['OrigArtist']

    def delete(self, m_id):
        """Delete an artist, song pair.

        Parameters
        ----------
        m_id: string
            The UUID of this song in the music database.

        Returns
        -------
        Does not return anything. The music delete operation
        always returns 200, HTTP success.
        """
        requests.delete(
            self._url + m_id,
            headers={'Authorization': self._auth}
        )
