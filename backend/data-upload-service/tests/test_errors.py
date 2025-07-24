import pytest
from src.errors.errors import APIError, BadRequest, NotFound, Forbidden

class TestAPIErrors:
    """Pruebas para las clases de error personalizadas"""
    
    def test_api_error_base_class(self):
        """Test de la clase base APIError"""
        error = APIError()
        
        assert error.code == 400
        assert error.description == 'API Error'
        assert isinstance(error, Exception)
    
    def test_api_error_custom_description(self):
        """Test de APIError con descripción personalizada"""
        custom_description = 'Error personalizado'
        error = APIError(custom_description)
        
        assert error.description == custom_description
        assert error.code == 400
    
    def test_bad_request_error(self):
        """Test de la clase BadRequest"""
        error = BadRequest()
        
        assert error.code == 400
        assert error.description == 'Bad request'
        assert isinstance(error, APIError)
    
    def test_bad_request_error_custom_message(self):
        """Test de BadRequest con mensaje personalizado"""
        custom_message = 'Archivo no válido'
        error = BadRequest(custom_message)
        
        assert error.description == custom_message
        assert error.code == 400
    
    def test_not_found_error(self):
        """Test de la clase NotFound"""
        error = NotFound()
        
        assert error.code == 404
        assert error.description == 'Not found'
        assert isinstance(error, APIError)
    
    def test_not_found_error_custom_message(self):
        """Test de NotFound con mensaje personalizado"""
        custom_message = 'Recurso no encontrado'
        error = NotFound(custom_message)
        
        assert error.description == custom_message
        assert error.code == 404
    
    def test_forbidden_error(self):
        """Test de la clase Forbidden"""
        error = Forbidden()
        
        assert error.code == 403
        assert error.description == 'Forbidden'
        assert isinstance(error, APIError)
    
    def test_forbidden_error_custom_message(self):
        """Test de Forbidden con mensaje personalizado"""
        custom_message = 'Acceso denegado'
        error = Forbidden(custom_message)
        
        assert error.description == custom_message
        assert error.code == 403
    
    def test_error_inheritance(self):
        """Test de la herencia de errores"""
        bad_request = BadRequest()
        not_found = NotFound()
        forbidden = Forbidden()
        
        # Todos deben ser instancias de APIError
        assert isinstance(bad_request, APIError)
        assert isinstance(not_found, APIError)
        assert isinstance(forbidden, APIError)
        
        # Y también instancias de Exception base
        assert isinstance(bad_request, Exception)
        assert isinstance(not_found, Exception)
        assert isinstance(forbidden, Exception)
    
    def test_error_with_werkzeug_exception(self):
        """Test de compatibilidad con HTTPException de Werkzeug"""
        from werkzeug.exceptions import HTTPException
        
        # Todos los errores deben ser instancias de HTTPException
        assert isinstance(APIError(), HTTPException)
        assert isinstance(BadRequest(), HTTPException)
        assert isinstance(NotFound(), HTTPException)
        assert isinstance(Forbidden(), HTTPException)
    
    def test_error_codes_are_correct(self):
        """Test de que los códigos de estado HTTP son correctos"""
        errors_and_codes = [
            (APIError(), 400),
            (BadRequest(), 400),
            (NotFound(), 404),
            (Forbidden(), 403)
        ]
        
        for error, expected_code in errors_and_codes:
            assert error.code == expected_code
    
    def test_error_string_representation(self):
        """Test de la representación string de los errores"""
        custom_message = 'Mensaje de prueba'
        
        errors = [
            BadRequest(custom_message),
            NotFound(custom_message),
            Forbidden(custom_message)
        ]
        
        for error in errors:
            # La representación string debe incluir el mensaje
            assert custom_message in str(error)
    
    def test_error_can_be_caught_as_api_error(self):
        """Test de que todos los errores se pueden capturar como APIError"""
        errors = [BadRequest(), NotFound(), Forbidden()]
        
        for error in errors:
            try:
                raise error
            except APIError as caught_error:
                assert isinstance(caught_error, type(error))
            except Exception:
                pytest.fail(f"Error {type(error)} no se pudo capturar como APIError")
    
    def test_multiple_error_handling(self):
        """Test de manejo de múltiples tipos de error"""
        def raise_bad_request():
            raise BadRequest('Bad request test')
        
        def raise_not_found():
            raise NotFound('Not found test')
        
        def raise_forbidden():
            raise Forbidden('Forbidden test')
        
        # Test que se pueden capturar específicamente
        with pytest.raises(BadRequest):
            raise_bad_request()
        
        with pytest.raises(NotFound):
            raise_not_found()
        
        with pytest.raises(Forbidden):
            raise_forbidden()
        
        # Test que se pueden capturar genéricamente como APIError
        for raise_func in [raise_bad_request, raise_not_found, raise_forbidden]:
            with pytest.raises(APIError):
                raise_func()
