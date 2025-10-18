# Security Policy

## Security Summary

GeniusDNA takes security seriously. This document outlines known vulnerabilities and recommended security practices.

## Known Vulnerabilities and Remediation

### Current Dependency Vulnerabilities

The requirements.txt has been updated to address known security vulnerabilities:

#### 1. FastAPI ReDoS Vulnerability
- **Affected versions**: <= 0.109.0
- **Patched version**: 0.109.1
- **CVE**: Content-Type Header ReDoS
- **Status**: ✅ Fixed in requirements.txt
- **Action**: Run `pip install --upgrade fastapi==0.109.1`

#### 2. python-multipart Vulnerabilities
- **Affected versions**: < 0.0.18
- **Patched version**: 0.0.18
- **CVE**: Multiple issues including DoS and ReDoS
- **Status**: ✅ Fixed in requirements.txt
- **Action**: Run `pip install --upgrade python-multipart==0.0.18`

### Installation with Secure Dependencies

To install with all security patches:

```bash
pip install -r requirements.txt
```

If you already have the project installed, upgrade dependencies:

```bash
pip install --upgrade fastapi==0.109.1 python-multipart==0.0.18
```

## Security Best Practices

### For Deployment

1. **Environment Variables**: Never commit sensitive data
   - Use `.env` files (already in .gitignore)
   - Set environment variables in production

2. **File Upload Security**:
   - The API accepts only text-based DNA files
   - Maximum file size should be enforced (recommended: 100MB)
   - Validate file content before processing

3. **API Security**:
   - Add authentication/authorization for production use
   - Implement rate limiting to prevent abuse
   - Use HTTPS in production
   - Configure CORS appropriately (currently set to allow all origins)

4. **Data Privacy**:
   - DNA data is highly sensitive personal information
   - Implement proper data retention policies
   - Ensure GDPR/HIPAA compliance if applicable
   - Use encryption for stored DNA data

5. **Database Security**:
   - Current implementation uses in-memory storage
   - For production, use a secure database with encryption
   - Implement proper access controls
   - Regular backups with encryption

### Recommended Production Configuration

```python
# app/main.py production settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domains only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Input Validation

The application implements:
- ✅ File format validation (23andMe and VCF)
- ✅ Genotype validation
- ✅ SNP ID validation
- ⚠️ File size limits (recommended to add)

## Reporting a Vulnerability

If you discover a security vulnerability in GeniusDNA:

1. **Do NOT** open a public issue
2. Email the security team (add contact info)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Checklist for Production

- [ ] Update all dependencies to latest secure versions
- [ ] Implement authentication/authorization
- [ ] Add rate limiting
- [ ] Configure CORS for specific origins
- [ ] Set up HTTPS with valid certificates
- [ ] Implement file size limits
- [ ] Add request validation middleware
- [ ] Set up logging and monitoring
- [ ] Implement data encryption at rest
- [ ] Regular security audits
- [ ] Backup and disaster recovery plan
- [ ] GDPR/HIPAA compliance review

## Dependencies Monitoring

We use the following tools to monitor dependencies:

- GitHub Dependabot
- Manual security audits
- PyPI advisory database

## Updates

Last security review: 2025-10-18
Last dependency update: 2025-10-18

## Compliance Considerations

GeniusDNA processes genetic data which may be subject to:

- **GDPR** (EU): Right to erasure, data portability, consent
- **HIPAA** (US): Protected Health Information (PHI) requirements
- **GINA** (US): Genetic Information Nondiscrimination Act

Consult with legal counsel before deploying in production.

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
