# School Lunch Alexa Skill

An Alexa skill that fetches and reads today's lunch menu from school cafeterias using the Nutrislice API.

## Project Structure

```
alexa-lunch/
├── api-notes.md              # Nutrislice API documentation and exploration
├── lambda/                   # AWS Lambda function code
│   ├── lambda_function.py    # Main Lambda handler
│   ├── requirements.txt      # Python dependencies (requests)
│   ├── test_local.py         # Local testing script
│   └── README.md             # Lambda documentation
├── terraform/                # Infrastructure-as-Code
│   ├── main.tf               # Terraform configuration
│   ├── variables.tf          # Input variables
│   ├── outputs.tf            # Output definitions
│   ├── terraform.tfvars.example  # Variable template
│   ├── DEPLOY.md             # Deployment guide
│   └── README.md             # Terraform documentation
└── README.md                 # This file
```

## Supported Schools

- **Los Cerros Middle** (San Ramon Valley USD)
- **Vista Grande Elementary** (San Ramon Valley USD)

## Features

✅ Fetches today's lunch menu from Nutrislice API
✅ Natural language responses ("lunch includes X, Y, and Z")
✅ Handles weekends/holidays gracefully
✅ Error handling for API timeouts
✅ Case-insensitive school name matching
✅ Filters for entrees only (no sides/beverages)

## Quick Start

### 1. Test Locally

```bash
cd lambda
python3 test_local.py
```

This will simulate Alexa requests and print responses.

### 2. Deploy to AWS

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your Alexa Skill ID
terraform init
terraform apply
```

See [terraform/DEPLOY.md](terraform/DEPLOY.md) for detailed deployment instructions.

### 3. Configure Alexa Skill

1. Copy the Lambda ARN from Terraform output
2. Go to https://developer.amazon.com/alexa/console/ask
3. Configure your skill's endpoint with the Lambda ARN
4. Test in the Alexa Simulator

## Example Interactions

**User:** "Alexa, open school lunch"
**Alexa:** "Which school's lunch would you like? You can ask about Los Cerros Middle or Vista Grande Elementary."

**User:** "What's for lunch at Los Cerros Middle?"
**Alexa:** "Today at Los Cerros Middle, lunch includes Chicken Teriyaki w/ White Rice, Cheese Focaccia Pizza, Turkey Sandwich, Yogurt Parfait, and Mac Salad."

**User:** "Vista Grande Elementary"
**Alexa:** "Today at Vista Grande Elementary, lunch includes Orange Chicken & Brown Rice and Cheese Pizza Slice."

## Architecture

```
Alexa Device
     ↓
Alexa Skills Kit (Amazon)
     ↓
AWS Lambda (school-lunch-skill)
     ↓
Nutrislice API (srvusd.api.nutrislice.com)
```

## Development

### Testing Locally

```bash
cd lambda
python3 test_local.py
```

### Updating the Lambda

1. Modify `lambda/lambda_function.py`
2. Run `terraform apply` in the `terraform/` directory
3. Terraform will detect changes and update the Lambda function

### API Documentation

See [api-notes.md](api-notes.md) for complete Nutrislice API documentation.

## Cost

**$0/month** - This project stays well within AWS Free Tier:
- Lambda: 1M free requests/month
- CloudWatch: 5GB free logs/month

## Files

| File | Purpose |
|------|---------|
| `api-notes.md` | Nutrislice API documentation |
| `lambda/lambda_function.py` | Lambda handler code |
| `lambda/requirements.txt` | Python dependencies |
| `lambda/test_local.py` | Local test suite |
| `terraform/main.tf` | Terraform infrastructure |
| `terraform/DEPLOY.md` | Deployment guide |

## Requirements

- Python 3.12+
- Terraform >= 1.5.0
- AWS CLI configured
- Alexa Developer account

## Deployment

See [terraform/DEPLOY.md](terraform/DEPLOY.md) for complete deployment instructions.

## License

This is a personal project for educational purposes.

## Contributing

This is a personal project, but feel free to fork and adapt for your own school district!

## Support

For issues:
- **Lambda code:** Test with `lambda/test_local.py`
- **API issues:** Check `api-notes.md`
- **Deployment:** See `terraform/DEPLOY.md`
- **AWS/Terraform:** Check CloudWatch logs

---

Built with ❤️ for students and parents in San Ramon Valley USD
